"""
Deterministic adjudication engine for GHOST TRACER.
Evaluates request eligibility, findings, policy rules, and recreation risks
to compute the audit status (COMPLETE, INCOMPLETE, NOT_APPLICABLE) and decision trace.
"""

from typing import Dict, List, Any
from .planner import plan_remediation

class Adjudicator:
    def adjudicate(self, request: Dict[str, Any], intent_res: Dict[str, Any], identity: Dict[str, Any],
                   scan_res: Dict[str, Any], risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Determines the audit verdict and remediation steps.
        """
        decision_trace = []
        case_id = request.get("case_id", "")

        # 1. Check intent authorization
        if not intent_res["is_deletion"]:
            decision_trace.append(f"RULE_001_INTENT: Request does not authorize deletion ({intent_res.get('reason', 'Non-deletion')}). Assigned NOT_APPLICABLE.")
            return {
                "case_id": case_id,
                "deletion_status": "NOT_APPLICABLE",
                "steps": [],
                "decision_trace": decision_trace,
                "confidence": 1.0,
                "findings_count": 0,
                "recreation_risks_count": 0
            }

        decision_trace.append(f"RULE_002_INTENT_CONFIRMED: Authorized deletion intent detected (Language: {intent_res.get('language')}).")

        findings = scan_res.get("findings", [])
        verifications = scan_res.get("verifications", [])

        # 2. Check for findings (remaining records, exposed PII)
        if findings:
            for f in findings:
                decision_trace.append(f"RULE_003_FINDING: {f['operation']} in {f['system_id']} ({f['resource_id']}) cited by {f.get('evidence_id')}.")

        # 3. Check for active recreation / restore risks
        if risks:
            for r in risks:
                decision_trace.append(f"RULE_004_LIFECYCLE_RISK: {r['risk_type']} in {r['system_id']} cited by {r.get('evidence_id')}.")

        has_violations = bool(findings or risks)

        if has_violations:
            status = "INCOMPLETE"
            decision_trace.append("RULE_005_ADJUDICATION: Policy violations or active recreation risks detected. Status set to INCOMPLETE.")
            steps = plan_remediation(findings, risks, is_complete=False, verifications=verifications)
        else:
            status = "COMPLETE"
            decision_trace.append("RULE_006_ADJUDICATION: All systems verified compliant at audit_at. Zero recreation risks. Status set to COMPLETE.")
            steps = plan_remediation(findings, risks, is_complete=True, verifications=verifications)

        return {
            "case_id": case_id,
            "deletion_status": status,
            "steps": steps,
            "decision_trace": decision_trace,
            "confidence": 0.98 if status == "COMPLETE" else 1.0,
            "findings_count": len(findings),
            "recreation_risks_count": len(risks)
        }
