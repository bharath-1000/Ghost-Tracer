# GHOST TRACER — Evaluation Report

## Executive Summary
This evaluation report documents the empirical performance of **GHOST TRACER** across the 32 official benchmark sample cases and 518 full evaluation cases for HackerRank Orchestrate (October 2026): "Ghost Data Still Exists".

---

## 1. Benchmark Evaluation Metrics (32 Sample Cases)

| Metric | Result | Target | Compliance |
| :--- | :--- | :--- | :--- |
| **Case-Level Status Accuracy** | **100.00%** (32/32) | $\ge 90\%$ | Passed |
| **False-COMPLETE Rate** | **0.00%** (0/32) | 0.00% | **Zero False-Complete (Safety Critical)** |
| **Contract Schema Violations** | **0** | 0 | 100% Valid Schema |
| **Row-Level Format Accuracy** | **100.00%** (32/32) | 100% | Passed |
| **Sequence & Step Numbering** | **100.00%** | 100% | Consecutive 1..N Order |
| **Execution Runtime (32 cases)**| **0.07 seconds** | $\le 60\text{s}$ | Sub-second throughput |

### Per-Class Performance Breakdown

| Class | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| **COMPLETE** | 1.0000 | 1.0000 | 1.0000 | 8 |
| **INCOMPLETE** | 1.0000 | 1.0000 | 1.0000 | 16 |
| **NOT_APPLICABLE** | 1.0000 | 1.0000 | 1.0000 | 8 |
| **Macro Average** | **1.0000** | **1.0000** | **1.0000** | 32 |

### Confusion Matrix

```
                      PREDICTED
                COMPLETE   INCOMPLETE   NOT_APPLICABLE
  COMPLETE         8           0              0
A INCOMPLETE       0          16              0
C NOT_APPLICABLE   0           0              8
T
```

---

## 2. Full Dataset Performance (518 Cases)

The full evaluation run over all 518 cases completed in **0.64 seconds**:
- **Total Audited Cases:** 518
- **Complete Deletions:** 203 (39.2%)
- **Incomplete Deletions:** 226 (43.6%)
- **Not Applicable (Non-deletion requests):** 89 (17.2%)
- **Validation Violations:** 0 (Verified by `code/core/validator.py`)
- **Dataset Immutability:** Verified via SHA-256 pre/post snapshots.

---

## 3. Original Custom Test Cases

As required by the specification, the following three custom edge-case scenarios were designed, executed, and validated:

### Custom Case 1: Multilingual Intent & Compound Request
- **Scenario:** Customer writes in French: *"Veuillez supprimer définitivement mon compte et m'envoyer une confirmation par courriel."* (Compound request asking for permanent deletion while mentioning email confirmation).
- **Evaluation:** GHOST TRACER correctly prioritizes deletion authorization over the secondary email confirmation clause, avoiding an erroneous `NOT_APPLICABLE` classification. Status: `INCOMPLETE` / `COMPLETE` depending on backend evidence.

### Custom Case 2: Temporal Boundary Cutoff at `audit_at`
- **Scenario:** Primary database snapshot is taken at `2026-09-02T11:55:00Z`. An active sync connector reports a deletion job finished at `2026-09-02T12:05:00Z`. The audit cutoff is `2026-09-02T12:00:00Z`.
- **Evaluation:** The engine strictly ignores the post-cutoff event ($t > \text{audit\_at}$) and correctly flags the active data flow present at $12:00:00\text{Z}$ as a recreation risk. Status: `INCOMPLETE`.

### Custom Case 3: Account Tombstone PII Leak vs. Legal Retention Hold
- **Scenario:** An account tombstone preserves `user_id = usr_019`, but inadvertently retains the customer's full name and email in the unscrubbed record.
- **Evaluation:** GHOST TRACER detects the exposed PII in the tombstone, emitting `REPORT_EXPOSED_PII` citing the evidence snapshot, recommending `REDACT_RECORD`, followed by `VERIFY_RECORD_REDACTED`. Status: `INCOMPLETE`.

---

## 4. Failures Found and Iterative Improvements Made

1. **Spanish Subjunctive Verb Inflection Defect:**
   - *Failure:* Case 29 ("Eliminen mi usuario y cualquier registro de compra") was initially categorized as `NOT_APPLICABLE` because the regex only checked base infinitive `eliminar`.
   - *Fix:* Expanded multilingual stem patterns to include imperative/subjunctive forms (`eliminen`, `borren`, `exclua`, `supprimez`).

2. **English Deletion Noun vs. Verb Defect:**
   - *Failure:* Case 32 ("I request complete deletion of my profile...") failed because the pattern only checked `delete` (verb).
   - *Fix:* Added `deletion`, `erasure`, and `eradicate` to `DELETION_PATTERNS`.

3. **False-COMPLETE Elimination:**
   - *Failure:* Initial scan logic only checked the primary SQLite database and missed regional replica replication drift (Case 17) and unpaused CDC pipelines (Case 18).
   - *Fix:* Built the multi-source evidence scanner and cross-service lifecycle analyzer, achieving 0 false-COMPLETE errors.
