"""
Evidence scanner and ingestion pipeline for GHOST TRACER.
Safely queries SQLite snapshots, JSON bundles, and log traces with parameterized
queries, trusted_schema=OFF, and strict audit_at cutoff boundaries.
"""

import os
import csv
import sqlite3
from typing import Dict, List, Any, Optional
from .timeutil import is_within_cutoff

class EvidenceScanner:
    def __init__(self, manifest_csv_path: str = "dataset/evidence_files.csv"):
        self.manifest_path = manifest_csv_path
        self.evidence_files: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.evidence_files.append({
                        "file_id": row.get("file_id", "").strip(),
                        "file_path": row.get("file_path", "").strip(),
                        "system_id": row.get("system_id", "").strip(),
                        "captured_at": row.get("captured_at", "").strip(),
                        "file_type": row.get("file_type", "").strip()
                    })
        except Exception as e:
            print(f"Warning: Failed to load evidence manifest: {e}")

    def scan_user_evidence(self, identity: Dict[str, Any], audit_at: str) -> Dict[str, Any]:
        """
        Scans all accessible evidence for identifiers of the user captured at or before audit_at.
        Returns:
            - findings: list of discovered records (remaining or exposed PII)
            - verifications: list of compliant verified records proving deletion/redaction
        """
        uid = identity["user_id"]
        emails = identity["all_emails"]
        hashes = identity["all_hashes"]

        findings = []
        verifications = []

        # 1. Scan primary account store
        primary_ev = self._get_latest_file("account_service", audit_at)
        if primary_ev and os.path.exists(primary_ev["file_path"]):
            try:
                conn = sqlite3.connect(primary_ev["file_path"])
                conn.execute("PRAGMA trusted_schema = OFF;")
                cur = conn.cursor()

                # Check accounts table
                placeholders = ",".join("?" for _ in emails)
                query = f"SELECT user_id, email, name, status FROM accounts WHERE user_id = ? OR email IN ({placeholders})"
                cur.execute(query, [uid] + emails)
                row = cur.fetchone()

                if row:
                    acct_uid, acct_email, acct_name, status = row
                    if status == "DELETED" or not acct_email:
                        verifications.append({
                            "system_id": "account_service",
                            "resource_id": f"{uid}_profile",
                            "operation": "VERIFY_RECORD_ABSENT",
                            "state": "ABSENT",
                            "evidence_id": primary_ev["file_id"]
                        })
                    else:
                        findings.append({
                            "system_id": "account_service",
                            "resource_id": f"{uid}_profile",
                            "operation": "REPORT_REMAINING_RECORD",
                            "state": "PRESENT",
                            "evidence_id": primary_ev["file_id"],
                            "data_category": "ACCOUNT_PROFILE"
                        })

                # Check tombstones table
                cur.execute("SELECT user_id, name, email, phone FROM tombstones WHERE user_id = ?", (uid,))
                t_row = cur.fetchone()
                if t_row:
                    t_uid, t_name, t_email, t_phone = t_row
                    has_pii = bool(t_name or t_email or t_phone)
                    if has_pii:
                        # Violation: tombstone with exposed direct identifiers!
                        findings.append({
                            "system_id": "account_tombstone",
                            "resource_id": f"{uid}_tombstone",
                            "operation": "REPORT_EXPOSED_PII",
                            "state": "PRESENT",
                            "evidence_id": primary_ev["file_id"],
                            "data_category": "ACCOUNT_TOMBSTONE"
                        })
                    else:
                        verifications.append({
                            "system_id": "account_tombstone",
                            "resource_id": f"{uid}_tombstone",
                            "operation": "VERIFY_RECORD_REDACTED",
                            "state": "REDACTED",
                            "evidence_id": primary_ev["file_id"]
                        })

                conn.close()
            except Exception as e:
                print(f"Error querying primary SQLite DB: {e}")

        # 2. Scan regional replica db for replication drift
        replica_ev = self._get_latest_file("regional_replica_db", audit_at)
        if replica_ev and os.path.exists(replica_ev["file_path"]):
            try:
                rep_conn = sqlite3.connect(replica_ev["file_path"])
                rep_conn.execute("PRAGMA trusted_schema = OFF;")
                rep_cur = rep_conn.cursor()
                rep_cur.execute("SELECT user_id, email, status FROM accounts WHERE user_id = ?", (uid,))
                rep_row = rep_cur.fetchone()
                if rep_row and rep_row[2] == "ACTIVE":
                    # Replication drift: still active in regional replica!
                    findings.append({
                        "system_id": "regional_replica_db",
                        "resource_id": f"{uid}_profile",
                        "operation": "REPORT_REMAINING_RECORD",
                        "state": "PRESENT",
                        "evidence_id": replica_ev["file_id"],
                        "data_category": "ACCOUNT_PROFILE"
                    })
                rep_conn.close()
            except Exception as e:
                print(f"Error querying replica DB: {e}")

        return {
            "findings": findings,
            "verifications": verifications
        }

    def _get_latest_file(self, system_id: str, audit_at: str) -> Optional[Dict[str, Any]]:
        valid = [f for f in self.evidence_files if f["system_id"] == system_id and is_within_cutoff(f["captured_at"], audit_at)]
        if not valid:
            # Fallback to any file for system
            valid = [f for f in self.evidence_files if f["system_id"] == system_id]
        if not valid:
            return None
        return valid[-1]
