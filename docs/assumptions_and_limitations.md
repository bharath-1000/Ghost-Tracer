# Assumptions and Limitations

### Key Assumptions
1. **Time Cutoff Boundary**: The `audit_at` timestamp is inclusive ($t \le \text{audit\_at}$). Any evidence or system activity timestamped strictly greater than `audit_at` is ignored during adjudication.
2. **Deterministic Baseline**: All primary policy, identity, lifecycle, and remediation decisions are computed 100% deterministically without relying on external LLM availability. Optional LLM inference is restricted to qualitative semantic explanations and conversational intent summaries.
3. **Audit-Only Boundary**: GHOST TRACER never mutates source data, executes deletion scripts, triggers API calls to modify live databases, or disables production pipelines. All remediation actions are strictly recommendations.
4. **Account Tombstones**: An account tombstone is compliant if and only if direct personal identifiers (`name`, `email`, `phone`, `email_hash`) are redacted/absent, even while the stable internal reference (`user_id`) is retained.

### Limitations
1. In development environments without binary OCR dependencies (`tesseract`), image screenshots are processed via structured OCR text extraction layers and manifests.
2. Hash collision: Email hashes are treated as case-insensitive 64-character hexadecimal strings (SHA-256).
3. Ambiguous Identifiers: When two distinct users share an identifier (e.g., duplicate phone entries), the link is marked ambiguous and unmerged to prevent unauthorized cross-user disclosures.
