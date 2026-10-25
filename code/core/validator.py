"""
Contract validator for GHOST TRACER.
Exhaustively checks output.csv against all HackerRank challenge specifications.
"""

import csv
import json
from typing import List, Dict, Any, Tuple

VALID_STATUSES = {"COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"}
VALID_PHASES = {"FINDING", "REMEDIATION", "VERIFICATION"}
VALID_OPERATIONS = {
    "REPORT_REMAINING_RECORD", "REPORT_EXPOSED_PII", "REPORT_ACTIVE_DATA_FLOW", "REPORT_RESTORE_RISK",
    "DISABLE_DATA_FLOW", "BLOCK_RESTORE", "DELETE_RECORD", "REDACT_RECORD", "ANONYMIZE_RECORD",
    "VERIFY_RECORD_ABSENT", "VERIFY_RECORD_PRESENT", "VERIFY_RECORD_REDACTED", "VERIFY_RECORD_ANONYMIZED",
    "VERIFY_DATA_FLOW_DISABLED", "VERIFY_RESTORE_BLOCKED"
}
VALID_STATES = {"PRESENT", "ABSENT", "REDACTED", "ANONYMIZED", "ACTIVE", "DISABLED", "BLOCKED"}
EXACT_KEYS = {"step_no", "phase", "system_id", "resource_id", "operation", "state", "evidence_id"}

def validate_output_file(file_path: str, expected_count: int = 518) -> Tuple[bool, List[str]]:
    violations = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header != ["case_id", "deletion_status", "steps_json"]:
                violations.append(f"Header mismatch: expected ['case_id', 'deletion_status', 'steps_json'], got {header}")

            row_count = 0
            prev_case_id = ""

            for line_no, row in enumerate(reader, start=2):
                row_count += 1
                if len(row) != 3:
                    violations.append(f"Line {line_no}: Expected 3 columns, got {len(row)}")
                    continue

                case_id, status, steps_str = row[0].strip(), row[1].strip(), row[2].strip()

                # Sorting check
                if prev_case_id and case_id < prev_case_id:
                    violations.append(f"Line {line_no}: case_id out of order: {case_id} after {prev_case_id}")
                prev_case_id = case_id

                # Status check
                if status not in VALID_STATUSES:
                    violations.append(f"Line {line_no}: Invalid status '{status}' for {case_id}")

                # steps_json check
                if status == "NOT_APPLICABLE":
                    if steps_str != "[]":
                        violations.append(f"Line {line_no}: NOT_APPLICABLE case {case_id} must have steps_json '[]', got '{steps_str}'")
                    continue

                try:
                    steps = json.loads(steps_str)
                except Exception as e:
                    violations.append(f"Line {line_no}: Invalid JSON in {case_id}: {e}")
                    continue

                if not isinstance(steps, list):
                    violations.append(f"Line {line_no}: steps_json in {case_id} is not an array")
                    continue

                for idx, step in enumerate(steps, start=1):
                    if not isinstance(step, dict):
                        violations.append(f"Line {line_no}: Step {idx} is not an object")
                        continue

                    # Exact 7 keys check
                    step_keys = set(step.keys())
                    if step_keys != EXACT_KEYS:
                        diff = step_keys.symmetric_difference(EXACT_KEYS)
                        violations.append(f"Line {line_no}: Step {idx} key mismatch for {case_id}: differences {diff}")

                    # Consecutive step_no check
                    if step.get("step_no") != idx:
                        violations.append(f"Line {line_no}: Step numbering non-consecutive: expected {idx}, got {step.get('step_no')}")

                    # Phase check
                    phase = step.get("phase")
                    if phase not in VALID_PHASES:
                        violations.append(f"Line {line_no}: Step {idx} invalid phase '{phase}'")

                    # Operation check
                    op = step.get("operation")
                    if op not in VALID_OPERATIONS:
                        violations.append(f"Line {line_no}: Step {idx} invalid operation '{op}'")

                    # State check
                    state = step.get("state")
                    if state not in VALID_STATES:
                        violations.append(f"Line {line_no}: Step {idx} invalid state '{state}'")

                    # Evidence citation rules
                    ev_id = step.get("evidence_id")
                    if status == "COMPLETE":
                        if phase != "VERIFICATION":
                            violations.append(f"Line {line_no}: COMPLETE case {case_id} has non-VERIFICATION step {phase}")
                        if not ev_id:
                            violations.append(f"Line {line_no}: COMPLETE case {case_id} step {idx} must cite evidence")
                    elif status == "INCOMPLETE":
                        if phase in ["REMEDIATION", "VERIFICATION"] and ev_id != "":
                            violations.append(f"Line {line_no}: INCOMPLETE case {case_id} future step {idx} must have evidence_id=''")

            if expected_count and row_count != expected_count:
                violations.append(f"Expected {expected_count} rows, found {row_count}")

    except Exception as e:
        violations.append(f"Failed to read/validate output file: {e}")

    return len(violations) == 0, violations
