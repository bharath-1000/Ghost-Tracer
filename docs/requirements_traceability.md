# Requirements Traceability Matrix

| Req ID | Requirement Description | Source | Implementation Module | Verification Test / Method |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Strict output schema: `case_id,deletion_status,steps_json` | Problem Statement §Output | `code/core/validator.py`, `code/core/serializer.py` | `test_output_csv_schema_and_headers` |
| **REQ-02** | Exact 3 statuses: `COMPLETE`, `INCOMPLETE`, `NOT_APPLICABLE` | Problem Statement §Output | `code/core/adjudicator.py` | `test_adjudication_status_values` |
| **REQ-03** | `NOT_APPLICABLE` produces exactly `[]` for `steps_json` | Problem Statement §Output | `code/core/intent.py`, `code/core/planner.py` | `test_not_applicable_steps_empty_array` |
| **REQ-04** | Multilingual intent detection with negation & withdrawal | Spec §5.1, Problem Statement | `code/core/intent.py` | `test_multilingual_intents_and_negation` |
| **REQ-05** | Historical identity resolution (email, phone, user_id, hash) | Spec §5.2, Problem Statement | `code/core/identity.py` | `test_identity_graph_traversal` |
| **REQ-06** | Temporal boundary: evidence captured after `audit_at` excluded | Spec §5.3, Problem Statement | `code/core/timeutil.py`, `code/core/evidence_scanner.py` | `test_temporal_cutoff_boundary` |
| **REQ-07** | Dynamic policy evaluation based on `deletion_rules.csv` | Spec §5.4, Problem Statement | `code/core/policy.py` | `test_dynamic_deletion_rules` |
| **REQ-08** | Account tombstone rules: stable `user_id` permitted, PII redacted | Problem Statement §Rules | `code/core/policy.py`, `code/core/adjudicator.py` | `test_tombstone_pii_redaction` |
| **REQ-09** | Recreation risk analysis: active syncs, connectors, restore jobs | Problem Statement §What to Build | `code/core/lifecycle.py` | `test_recreation_path_detection` |
| **REQ-10** | Deterministic adjudication with zero LLM dependence | Spec §5.6 | `code/core/adjudicator.py` | `test_deterministic_adjudication` |
| **REQ-11** | Ordered remediation plan: FINDING -> REMEDIATION -> VERIFICATION | Problem Statement §Allowed Ops | `code/core/planner.py` | `test_steps_phase_and_op_sorting` |
| **REQ-12** | Valid 7-key JSON step objects | Problem Statement §Output | `code/core/serializer.py`, `code/core/validator.py` | `test_step_json_exact_keys` |
| **REQ-13** | Evidence citation: COMPLETE verification cites evidence; future steps use `""` | Problem Statement §Rules | `code/core/planner.py` | `test_evidence_citation_rules` |
| **REQ-14** | Audit-only boundary: zero execution of deletions/mutations | Spec §1 | Entire system | `test_no_destructive_endpoints` |
| **REQ-15** | Dataset immutability & hash verification | Spec §8.4, §8.5 | `code/core/security.py` | `test_dataset_immutability_hash` |
| **REQ-16** | 100% evaluated benchmark on sample requests | Spec §10.1 | `code/evaluation/evaluate.py` | Sample suite regression runner |
