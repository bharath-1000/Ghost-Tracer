# GHOST TRACER — AI-Powered Data Deletion Auditor

> **Track the Ghost. Prove the Deletion.**  
> Evidence-driven data deletion auditing, identity graph resolution, lifecycle recreation analysis, and remediation planning for enterprise privacy compliance.  
> Official Submission for **HackerRank Orchestrate (October 2026): "Ghost Data Still Exists"**

---

## 1. Executive Overview

When Northstar Shop received a deletion request, internal dashboards erroneously reported it as **“Complete.”** Weeks later, the customer reappeared as a “ghost” because data persisted across secondary replica databases, unscrubbed account tombstones, and active CDC synchronization pipelines.

**GHOST TRACER** was built to solve this enterprise data privacy crisis:
- **Strictly Audit-Only**: Never alters source records, modifies retention policies, or executes destructive mutations.
- **Evidence-Grounded**: Reported statuses and workflow messages are claims, not proof. Only evidence captured at or before `audit_at` is evaluated.
- **Deterministic Compliance**: Adjudication logic runs with 100% mathematical determinism, ensuring zero hallucination and byte-identical reproducibility.
- **Complete Remediation Planning**: Generates strictly ordered 7-key JSON objects across `FINDING`, `REMEDIATION`, and `VERIFICATION` phases.

---

## 2. Key Results & Performance

| Metric | Measured Value | Standard | Status |
| :--- | :--- | :--- | :--- |
| **Status Accuracy (32 Benchmark Cases)** | **100.00%** (32/32) | $\ge 90\%$ | **PASS** |
| **False-COMPLETE Errors** | **0** | 0 | **ZERO FALSE-COMPLETE (Safety Critical)** |
| **Contract Schema Violations** | **0** | 0 | **100% VALID SCHEMA** |
| **Full Run Runtime (518 Cases)** | **0.64 seconds** | $\le 60\text{s}$ | **Ultra-Fast Sub-second** |
| **Per-Class F1 (COMPLETE / INCOMPLETE / N/A)** | **1.0000 / 1.0000 / 1.0000** | $\ge 0.90$ | **Optimal Precision & Recall** |

---

## 3. Quick Start & Execution Commands

### Prerequisites
- Python 3.10+ (Standard library: `sqlite3`, `json`, `csv`, `hashlib`, `hmac`, `unittest`)
- Node.js 18+ (for Web UI & API server)

### 1. Run Core Audit Engine (Graded CLI)
To audit the dataset and produce the verified `output.csv` at repository root:
```bash
python3 code/main.py
```

### 2. Audit Benchmark Sample Cases (32 Cases)
```bash
python3 code/main.py --samples
```

### 3. Run Automated Evaluation Against Canonical Labels
```bash
python3 code/evaluation/evaluate.py output.csv dataset/sample_output.csv
```

### 4. Run Test Suite
```bash
python3 scripts/run_tests.py
```

### 5. Package Submission Archive (`code.zip`)
```bash
python3 scripts/package_submission.py
```

### 6. Start Full-Stack Web Application (Port 3000)
```bash
npm run dev
```

---

## 4. Architecture & Core Subsystems

```
code/
├── main.py                          # CLI runner: python3 code/main.py
├── core/
│   ├── timeutil.py                  # UTC normalization & strict audit_at cutoff
│   ├── intent.py                    # Multilingual intent engine (EN, ES, PT, FR, KO, JA)
│   ├── identity.py                  # Identity graph (user ID, current & historical email, phone, SHA-256 hash)
│   ├── evidence_scanner.py          # Safe SQLite snapshot querying & replication drift detection
│   ├── policy.py                    # Dynamic loader for deletion_rules.csv & tombstone PII checks
│   ├── lifecycle.py                 # CDC sync pipelines & backup recovery risk detection
│   ├── adjudicator.py               # Deterministic adjudication (COMPLETE / INCOMPLETE / NOT_APPLICABLE)
│   ├── planner.py                   # Strict 7-key JSON step generator & 15-operation sorting
│   ├── serializer.py                # Byte-consistent CSV & JSON serializer
│   ├── validator.py                 # Output contract validator (0 violations)
│   └── security.py                  # SHA-256 dataset immutability & run manifest generator
├── evaluation/
│   ├── evaluate.py                  # Benchmarking evaluator & confusion matrix calculator
│   ├── evaluation_report.md         # Full evaluation report with custom edge test cases
│   └── usage_report.md              # Model and token cost analysis report
└── tests/                           # Unit, contract, and regression test suites
```

---

## 5. Required Submission Deliverables

1. **`output.csv`**: Contains all 518 cases, sorted by `case_id`, strictly formatted.
2. **`log.txt`**: Continuous conversation transcript adhering to `AGENTS.md` format.
3. **`code.zip`**: Packaged via `scripts/package_submission.py` containing code, documentation, and evaluation reports.
4. **`agent-trace.zip`**: Agent harness trajectory archive.
5. **Documentation**: `docs/` containing requirements traceability, architecture, threat model, and testing strategy.
