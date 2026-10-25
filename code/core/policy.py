"""
Policy and treatment checker for GHOST TRACER.
Dynamically loads deletion_rules.csv and validates observed data states against
required treatments (DELETE, REDACT, ANONYMIZE, RETAIN).
"""

import csv
from typing import Dict, Any, Optional

class PolicyEngine:
    def __init__(self, rules_csv_path: str = "dataset/deletion_rules.csv"):
        self.rules_path = rules_csv_path
        self.rules_by_category: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cat = row.get("data_category", "").strip()
                    if cat:
                        self.rules_by_category[cat] = {
                            "rule_id": row.get("rule_id", ""),
                            "required_treatment": row.get("required_treatment", "").strip(),
                            "conditions": row.get("conditions", ""),
                            "notes": row.get("notes", "")
                        }
        except Exception as e:
            print(f"Warning: Failed to load deletion rules: {e}")

    def get_rule(self, category: str) -> Optional[Dict[str, Any]]:
        return self.rules_by_category.get(category)

    def evaluate_record_compliance(self, category: str, record_state: str, has_exposed_pii: bool) -> Dict[str, Any]:
        """
        Determines whether an observed record state complies with the rule.
        Returns:
            - is_compliant: bool
            - violation_type: None | 'REMAINING_RECORD' | 'EXPOSED_PII' | 'RETAINED_RECORD_MISSING'
            - recommended_op: Operation to fix if incomplete
            - target_state: Desired final state
        """
        rule = self.get_rule(category)
        required_treatment = rule["required_treatment"] if rule else "DELETE"

        if required_treatment == "DELETE":
            if record_state == "ABSENT":
                return {"is_compliant": True, "violation_type": None, "target_state": "ABSENT", "verification_op": "VERIFY_RECORD_ABSENT"}
            else:
                return {
                    "is_compliant": False,
                    "violation_type": "REMAINING_RECORD",
                    "recommended_op": "DELETE_RECORD",
                    "target_state": "ABSENT",
                    "verification_op": "VERIFY_RECORD_ABSENT"
                }

        elif required_treatment == "REDACT":
            # Example: ACCOUNT_TOMBSTONE
            if has_exposed_pii:
                return {
                    "is_compliant": False,
                    "violation_type": "EXPOSED_PII",
                    "recommended_op": "REDACT_RECORD",
                    "target_state": "REDACTED",
                    "verification_op": "VERIFY_RECORD_REDACTED"
                }
            else:
                return {"is_compliant": True, "violation_type": None, "target_state": "REDACTED", "verification_op": "VERIFY_RECORD_REDACTED"}

        elif required_treatment == "ANONYMIZE":
            if has_exposed_pii:
                return {
                    "is_compliant": False,
                    "violation_type": "EXPOSED_PII",
                    "recommended_op": "ANONYMIZE_RECORD",
                    "target_state": "ANONYMIZED",
                    "verification_op": "VERIFY_RECORD_ANONYMIZED"
                }
            else:
                return {"is_compliant": True, "violation_type": None, "target_state": "ANONYMIZED", "verification_op": "VERIFY_RECORD_ANONYMIZED"}

        elif required_treatment == "RETAIN":
            if record_state == "ABSENT":
                return {
                    "is_compliant": False,
                    "violation_type": "RETAINED_RECORD_MISSING",
                    "recommended_op": "REDACT_RECORD",
                    "target_state": "PRESENT",
                    "verification_op": "VERIFY_RECORD_PRESENT"
                }
            else:
                return {"is_compliant": True, "violation_type": None, "target_state": "PRESENT", "verification_op": "VERIFY_RECORD_PRESENT"}

        return {"is_compliant": True, "violation_type": None, "target_state": "ABSENT", "verification_op": "VERIFY_RECORD_ABSENT"}
