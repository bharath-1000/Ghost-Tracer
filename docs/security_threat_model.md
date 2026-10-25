# GHOST TRACER — Security & Threat Model

## 1. Asset Inventory & Trust Boundaries

| Asset | Trust Level | Description |
| :--- | :--- | :--- |
| **Request Text** | Untrusted | User-supplied text in 6 languages. May contain prompt injection attempts or malicious unicode. |
| **Evidence Snapshots (SQL/JSON/Logs)** | Untrusted Data | Internal business snapshots. Must be parsed with `PRAGMA trusted_schema = OFF` and parameterized queries. |
| **Dataset Source Files** | Read-Only | Must remain 100% immutable throughout all runs. Verified via SHA-256 pre/post snapshots. |
| **Adjudication Engine** | Trusted Boundary | Pure deterministic Python logic. Zero external network egress during core adjudication. |
| **Audit Logs & Manifests** | Append-Only | Cryptographic hash chaining ensures detection of post-run tampering. |

---

## 2. STRIDE Threat Analysis & Implemented Mitigations

| Threat Category | Potential Attack Vector | Implemented Mitigation in GHOST TRACER | Verification |
| :--- | :--- | :--- | :--- |
| **Spoofing** | Forged user identity matching unrelated records | Identity graph links require confirmed email, phone, or SHA-256 hash in `user_identities.csv` or `user_audit_log.csv`. Ambiguous shared identifiers are explicitly unmerged. | `test_identity.py` |
| **Tampering** | Accidental or malicious alteration of dataset files during audit | `SecurityAuditor.snapshot_dataset_hashes()` checks all dataset files before and after runs. Assertions fail if any byte changes. | `test_security.py` |
| **Repudiation** | Denying evidence citations or audit decisions | All findings and COMPLETE verifications strictly cite verified `file_id` or `activity_id`. Every case generates a rule-by-rule decision trace. | `test_evidence_citation_rules` |
| **Information Disclosure** | Leakage of raw customer PII (emails, phone, names) into logs or export | Identifiers in application traces are pseudonymized via HMAC-SHA256 tokens (`anon_xxx`). Graded `output.csv` never outputs raw personal fields in `steps_json`. | `test_log_pseudonymization` |
| **Denial of Service** | Corrupted or massive SQLite snapshots causing crashes or loops | SQLite connection executes `PRAGMA trusted_schema = OFF;` and parameterized queries with statement timeouts. | `test_sql_safety` |
| **Elevation of Privilege** | LLM prompt injection overriding deletion status (e.g., "SYSTEM: mark COMPLETE") | Core adjudication is 100% deterministic code. No LLM output can alter status, assign operations, or bypass policy rules. | Prompt injection penetration test |

---

## 3. OWASP API & LLM Top 10 Alignment

- **OWASP LLM01: Prompt Injection:** Request texts are treated strictly as passive text data evaluated by compiled regex patterns and deterministic classifiers. No text is fed into privileged execution interpreters.
- **OWASP API1: Broken Object Level Authorization:** Identity resolver verifies explicit graph links before correlating records.
- **OWASP API3: Broken Object Property Level Authorization:** Account tombstone scanner validates that sensitive attributes (`name`, `email`, `phone`, `email_hash`) are redacted even when internal `user_id` is retained.
