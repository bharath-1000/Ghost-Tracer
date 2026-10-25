# GHOST TRACER — Technical Architecture

```
                          ┌─────────────────────────────────────┐
                          │         Web Client (React)          │
                          │   Dark Graphite & Cyan UI, WCAG AA   │
                          │   10 Integrated Audit Workspaces    │
                          └──────────────────┬──────────────────┘
                                             │ HTTP/JSON
                                             ▼
                          ┌─────────────────────────────────────┐
                          │   Node.js / Express Server (server.ts│
                          │   /api/v1 REST endpoints & Runner   │
                          └──────────────────┬──────────────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       ▼                                           ▼
         ┌───────────────────────────┐               ┌───────────────────────────┐
         │     Python CLI Runner     │               │    Direct Engine Service  │
         │       code/main.py        │               │    code/core & dataset    │
         └─────────────┬─────────────┘               └─────────────┬─────────────┘
                       │                                           │
                       └─────────────────────┬─────────────────────┘
                                             ▼
        ┌────────────────────────────────────────────────────────────────────────┐
        │                        Core Audit Pipeline                             │
        │                                                                        │
        │  1. Request Intake & Intent Engine (Multilingual, Negation, Withdrawal)│
        │  2. Identity Graph Resolver (Email, User ID, Phone, SHA-256 Hash)      │
        │  3. Evidence Scanning & Ingestion (SQL, JSON, Logs, Text, Docs)        │
        │  4. Temporal Normalization & Cutoff at audit_at                        │
        │  5. Policy Rule Checker (deletion_rules.csv, Tombstones, Holds)        │
        │  6. Lifecycle Recreation & Restore Risk Analyzer (system_activity.csv) │
        │  7. Deterministic Adjudication Logic (COMPLETE / INCOMPLETE / N/A)     │
        │  8. Remediation & Verification Planner (Strict Phase & Operation Order)│
        │  9. Output Serializer & Contract Validator (output.csv byte parity)    │
        │ 10. Security & Integrity Guard (SHA-256 Run Manifest, Immutability)    │
        └────────────────────────────────────┬───────────────────────────────────┘
                                             │
                                             ▼
                         ┌───────────────────────────────────────┐
                         │   dataset/  (Immutable read-only)     │
                         │   output.csv (Validated submission)   │
                         └───────────────────────────────────────┘
```

## Core Modules

- `code/core/timeutil.py`: UTC normalization, ISO-8601 parsing, strict cutoff enforcement at `audit_at`.
- `code/core/intent.py`: Deterministic multilingual NLP classifier covering English, Spanish, Portuguese, French, Korean, and Japanese. Accurately flags non-deletion requests (access, marketing opt-out, data export, account correction) as `NOT_APPLICABLE`, while respecting explicit negations and withdrawals.
- `code/core/identity.py`: Graph-based identity traversal joining `user_identities.csv` and `user_audit_log.csv`. Matches direct emails, historical alias emails, normalized phone numbers, internal `user_id`s, and hexadecimal email hashes.
- `code/core/evidence_scanner.py`: Ingests and searches evidence files. Parses SQLite snapshots, JSON exports, and log traces.
- `code/core/policy.py`: Loads `deletion_rules.csv` dynamically. Evaluates rule conditions, tombstone restrictions, and legal holds.
- `code/core/lifecycle.py`: Parses `system_activity.csv` for data sync connectors, CDC pipelines, and backup recovery routines active at `audit_at`.
- `code/core/adjudicator.py`: Purely deterministic decision engine. Never declares `COMPLETE` from claims alone; requires verifiable evidence for all in-scope systems.
- `code/core/planner.py`: Generates the strict 7-key JSON objects across `FINDING`, `REMEDIATION`, and `VERIFICATION` phases, applying exact sorting and evidence citation rules.
- `code/core/validator.py`: Comprehensive output contract validator ensuring zero grading violations.
- `code/core/security.py`: Immutability hashes, run manifest generator, and log pseudonymization.
