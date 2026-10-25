"""
Identity resolution graph engine for GHOST TRACER.
Reconstructs current and historical identifiers (user IDs, emails, phone numbers,
SHA-256 hashes) using user_identities.csv and user_audit_log.csv.
"""

import csv
import hashlib
from typing import Dict, List, Set, Optional, Any

def normalize_email(email: Optional[str]) -> str:
    if not email:
        return ""
    return email.strip().lower()

def compute_sha256(val: str) -> str:
    return hashlib.sha256(val.strip().lower().encode("utf-8")).hexdigest()

class IdentityResolver:
    def __init__(self, identities_csv_path: str = "dataset/user_identities.csv", audit_log_csv_path: str = "dataset/user_audit_log.csv"):
        self.identities_path = identities_csv_path
        self.audit_log_path = audit_log_csv_path
        self.users_by_id: Dict[str, Dict[str, Any]] = {}
        self.users_by_email: Dict[str, str] = {}
        self.users_by_hash: Dict[str, str] = {}
        self.audit_history: Dict[str, List[Dict[str, Any]]] = {}
        self._load()

    def _load(self):
        # Load current identities
        try:
            with open(self.identities_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    uid = row.get("user_id", "").strip()
                    if not uid:
                        continue
                    email = normalize_email(row.get("email"))
                    em_hash = row.get("email_hash", "").strip().lower()
                    if not em_hash and email:
                        em_hash = compute_sha256(email)

                    profile = {
                        "user_id": uid,
                        "name": row.get("name", "").strip(),
                        "email": email,
                        "phone": row.get("phone", "").strip(),
                        "email_hash": em_hash,
                        "updated_at": row.get("updated_at", "").strip(),
                        "historical_emails": set(),
                        "historical_phones": set(),
                        "provenance": []
                    }
                    self.users_by_id[uid] = profile
                    if email:
                        self.users_by_email[email] = uid
                    if em_hash:
                        self.users_by_hash[em_hash] = uid
        except Exception as e:
            print(f"Warning: Failed to load identities: {e}")

        # Load historical audit log
        try:
            with open(self.audit_log_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    uid = row.get("user_id", "").strip()
                    field = row.get("field_name", "").strip()
                    old_val = row.get("old_value", "").strip()
                    new_val = row.get("new_value", "").strip()
                    changed_at = row.get("changed_at", "").strip()
                    audit_id = row.get("audit_id", "").strip()

                    if uid not in self.audit_history:
                        self.audit_history[uid] = []
                    self.audit_history[uid].append({
                        "audit_id": audit_id,
                        "field": field,
                        "old_value": old_val,
                        "new_value": new_val,
                        "changed_at": changed_at
                    })

                    if uid in self.users_by_id:
                        if field == "email":
                            norm_old = normalize_email(old_val)
                            if norm_old:
                                self.users_by_id[uid]["historical_emails"].add(norm_old)
                                self.users_by_email[norm_old] = uid
                                self.users_by_hash[compute_sha256(norm_old)] = uid
                        elif field == "phone":
                            if old_val:
                                self.users_by_id[uid]["historical_phones"].add(old_val)
        except Exception as e:
            print(f"Warning: Failed to load audit log: {e}")

    def resolve(self, request_email: str) -> Optional[Dict[str, Any]]:
        norm = normalize_email(request_email)
        uid = self.users_by_email.get(norm)
        if not uid:
            # Check if matching hash
            em_hash = compute_sha256(norm)
            uid = self.users_by_hash.get(em_hash)

        if not uid or uid not in self.users_by_id:
            # Generate a provisional identity if absent
            return {
                "user_id": f"provisional_{compute_sha256(norm)[:8]}",
                "name": "",
                "email": norm,
                "phone": "",
                "email_hash": compute_sha256(norm),
                "historical_emails": [],
                "historical_phones": [],
                "all_emails": [norm],
                "all_hashes": [compute_sha256(norm)],
                "is_provisional": True,
                "audit_entries": []
            }

        prof = self.users_by_id[uid]
        all_emails = list({prof["email"]} | set(prof["historical_emails"]))
        all_hashes = list({compute_sha256(e) for e in all_emails if e} | ({prof["email_hash"]} if prof["email_hash"] else set()))

        return {
            "user_id": uid,
            "name": prof["name"],
            "email": prof["email"],
            "phone": prof["phone"],
            "email_hash": prof["email_hash"],
            "historical_emails": list(prof["historical_emails"]),
            "historical_phones": list(prof["historical_phones"]),
            "all_emails": [e for e in all_emails if e],
            "all_hashes": [h for h in all_hashes if h],
            "is_provisional": False,
            "audit_entries": self.audit_history.get(uid, [])
        }
