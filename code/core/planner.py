"""
Remediation and verification planner for GHOST TRACER.
Generates ordered, evidence-backed step objects conforming to the exact
7-key HackerRank JSON specification and sorting rules.
"""

from typing import List, Dict, Any

OPERATION_PRIORITY = {
    "REPORT_REMAINING_RECORD": 1,
    "REPORT_EXPOSED_PII": 2,
    "REPORT_ACTIVE_DATA_FLOW": 3,
    "REPORT_RESTORE_RISK": 4,
    "DISABLE_DATA_FLOW": 5,
    "BLOCK_RESTORE": 6,
    "DELETE_RECORD": 7,
    "REDACT_RECORD": 8,
    "ANONYMIZE_RECORD": 9,
    "VERIFY_RECORD_ABSENT": 10,
    "VERIFY_RECORD_PRESENT": 11,
    "VERIFY_RECORD_REDACTED": 12,
    "VERIFY_RECORD_ANONYMIZED": 13,
    "VERIFY_DATA_FLOW_DISABLED": 14,
    "VERIFY_RESTORE_BLOCKED": 15
}

PHASE_PRIORITY = {
    "FINDING": 1,
    "REMEDIATION": 2,
    "VERIFICATION": 3
}

def sort_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sorts steps by:
    1. Phase (FINDING, then REMEDIATION, then VERIFICATION)
    2. Operation (official 15-operation order)
    3. system_id ascending
    4. resource_id ascending
    """
    def sort_key(s):
        phase_order = PHASE_PRIORITY.get(s["phase"], 99)
        op_order = OPERATION_PRIORITY.get(s["operation"], 99)
        system_id = s.get("system_id", "")
        resource_id = s.get("resource_id", "")
        return (phase_order, op_order, system_id, resource_id)

    sorted_list = sorted(steps, key=sort_key)
    
    # Renumber consecutively starting from 1
    for idx, step in enumerate(sorted_list, start=1):
        step["step_no"] = idx

    return sorted_list

def plan_remediation(findings: List[Dict[str, Any]], risks: List[Dict[str, Any]], is_complete: bool, verifications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Builds the complete plan of 7-key JSON objects:
    step_no, phase, system_id, resource_id, operation, state, evidence_id
    """
    if is_complete:
        # COMPLETE case: only verified checks with real evidence IDs proving compliant state
        raw_steps = []
        for v in verifications:
            raw_steps.append({
                "phase": "VERIFICATION",
                "system_id": v["system_id"],
                "resource_id": v["resource_id"],
                "operation": v["operation"],
                "state": v["state"],
                "evidence_id": v.get("evidence_id", "")
            })
        return sort_steps(raw_steps)

    raw_steps = []

    # 1. Findings from lifecycle risks (active data flows and restore risks)
    for r in risks:
        raw_steps.append({
            "phase": "FINDING",
            "system_id": r["system_id"],
            "resource_id": r["resource_id"],
            "operation": r["operation_finding"],
            "state": "ACTIVE",
            "evidence_id": r.get("evidence_id", "")
        })

    # 2. Findings from residual records and exposed PII
    for f in findings:
        raw_steps.append({
            "phase": "FINDING",
            "system_id": f["system_id"],
            "resource_id": f["resource_id"],
            "operation": f["operation"],
            "state": f["state"],
            "evidence_id": f.get("evidence_id", "")
        })

    # 3. Remediation steps (evidence_id must be "")
    # Recreation risks are remediated first (disable flows, block restores)
    for r in risks:
        raw_steps.append({
            "phase": "REMEDIATION",
            "system_id": r["system_id"],
            "resource_id": r["resource_id"],
            "operation": r["operation_remediation"],
            "state": "DISABLED" if r["operation_remediation"] == "DISABLE_DATA_FLOW" else "BLOCKED",
            "evidence_id": ""
        })

    # Record remediation (DELETE, REDACT, ANONYMIZE)
    for f in findings:
        op = f["operation"]
        cat = f.get("data_category", "ACCOUNT_PROFILE")
        if op == "REPORT_REMAINING_RECORD":
            rem_op = "DELETE_RECORD"
            rem_state = "ABSENT"
        elif op == "REPORT_EXPOSED_PII":
            rem_op = "REDACT_RECORD" if cat == "ACCOUNT_TOMBSTONE" else "ANONYMIZE_RECORD"
            rem_state = "REDACTED" if rem_op == "REDACT_RECORD" else "ANONYMIZED"
        else:
            rem_op = "DELETE_RECORD"
            rem_state = "ABSENT"

        raw_steps.append({
            "phase": "REMEDIATION",
            "system_id": f["system_id"],
            "resource_id": f["resource_id"],
            "operation": rem_op,
            "state": rem_state,
            "evidence_id": ""
        })

    # 4. Future-state Verification steps (evidence_id must be "")
    for f in findings:
        op = f["operation"]
        cat = f.get("data_category", "ACCOUNT_PROFILE")
        if op == "REPORT_REMAINING_RECORD":
            ver_op = "VERIFY_RECORD_ABSENT"
            ver_state = "ABSENT"
        elif op == "REPORT_EXPOSED_PII":
            ver_op = "VERIFY_RECORD_REDACTED" if cat == "ACCOUNT_TOMBSTONE" else "VERIFY_RECORD_ANONYMIZED"
            ver_state = "REDACTED" if ver_op == "VERIFY_RECORD_REDACTED" else "ANONYMIZED"
        else:
            ver_op = "VERIFY_RECORD_ABSENT"
            ver_state = "ABSENT"

        raw_steps.append({
            "phase": "VERIFICATION",
            "system_id": f["system_id"],
            "resource_id": f["resource_id"],
            "operation": ver_op,
            "state": ver_state,
            "evidence_id": ""
        })

    for r in risks:
        raw_steps.append({
            "phase": "VERIFICATION",
            "system_id": r["system_id"],
            "resource_id": r["resource_id"],
            "operation": r["operation_verification"],
            "state": "DISABLED" if r["operation_verification"] == "VERIFY_DATA_FLOW_DISABLED" else "BLOCKED",
            "evidence_id": ""
        })

    return sort_steps(raw_steps)
