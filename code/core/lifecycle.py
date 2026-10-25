"""
Lifecycle & recreation analysis engine for GHOST TRACER.
Inspects system_activity.csv to identify active sync pipelines, CDC connectors,
backup restoration risks, and replication drift occurring before or at audit_at.
"""

import csv
from typing import Dict, List, Any
from .timeutil import is_within_cutoff

class LifecycleAnalyzer:
    def __init__(self, activity_csv_path: str = "dataset/system_activity.csv"):
        self.activity_path = activity_csv_path
        self.activities: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        try:
            with open(self.activity_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.activities.append({
                        "activity_id": row.get("activity_id", "").strip(),
                        "system_id": row.get("system_id", "").strip(),
                        "activity_type": row.get("activity_type", "").strip(),
                        "target_user_id": row.get("target_user_id", "").strip(),
                        "reported_result": row.get("reported_result", "").strip(),
                        "started_at": row.get("started_at", "").strip(),
                        "completed_at": row.get("completed_at", "").strip(),
                        "details": row.get("details", "").strip()
                    })
        except Exception as e:
            print(f"Warning: Failed to load system activity: {e}")

    def find_risks(self, user_id: str, audit_at: str) -> List[Dict[str, Any]]:
        """
        Scans activities targeting user_id that were active at audit_at.
        Returns list of risk descriptors.
        """
        risks = []
        for act in self.activities:
            if act["target_user_id"] != user_id:
                continue

            # Must start on or before audit_at
            if not is_within_cutoff(act["started_at"], audit_at):
                continue

            act_type = act["activity_type"]
            result = act["reported_result"]
            completed_at = act["completed_at"]
            is_active = (result in ["RUNNING", "STAGED", "ACTIVE"]) or (not completed_at) or (not is_within_cutoff(completed_at, audit_at))

            if "SYNC" in act_type or "REPLICATION" in act_type:
                if is_active:
                    risks.append({
                        "risk_type": "ACTIVE_DATA_FLOW",
                        "operation_finding": "REPORT_ACTIVE_DATA_FLOW",
                        "operation_remediation": "DISABLE_DATA_FLOW",
                        "operation_verification": "VERIFY_DATA_FLOW_DISABLED",
                        "system_id": act["system_id"],
                        "resource_id": f"flow_{user_id}",
                        "evidence_id": act["activity_id"],
                        "details": act["details"]
                    })

            elif "RESTORE" in act_type or "BACKUP" in act_type or "SNAPSHOT" in act_type:
                if is_active:
                    risks.append({
                        "risk_type": "RESTORE_RISK",
                        "operation_finding": "REPORT_RESTORE_RISK",
                        "operation_remediation": "BLOCK_RESTORE",
                        "operation_verification": "VERIFY_RESTORE_BLOCKED",
                        "system_id": act["system_id"],
                        "resource_id": f"backup_snapshot_{user_id}",
                        "evidence_id": act["activity_id"],
                        "details": act["details"]
                    })

        return risks
