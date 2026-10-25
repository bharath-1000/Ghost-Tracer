#!/usr/bin/env python3
"""
Evaluator for GHOST TRACER.
Evaluates predictions against sample_output.csv or labeled test sets.
Calculates status accuracy, per-class precision/recall/F1, confusion matrix,
false-COMPLETE count, step-level and sequence accuracy.
"""

import sys
import csv
import json
from collections import defaultdict
from typing import Dict, List, Any

def evaluate_predictions(predictions_csv: str = "output.csv", ground_truth_csv: str = "dataset/sample_output.csv") -> Dict[str, Any]:
    preds = {}
    with open(predictions_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            preds[row["case_id"]] = row

    truth = {}
    with open(ground_truth_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            truth[row["case_id"]] = row

    total_cases = len(truth)
    correct_status_count = 0
    false_complete_count = 0

    classes = ["COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"]
    confusion_matrix = {c1: {c2: 0 for c2 in classes} for c1 in classes}
    mismatches = []

    step_exact_matches = 0

    for cid, t_row in truth.items():
        if cid not in preds:
            mismatches.append({"case_id": cid, "issue": "Missing in predictions", "expected": t_row["deletion_status"], "actual": "NONE"})
            continue

        p_row = preds[cid]
        exp_status = t_row["deletion_status"]
        act_status = p_row["deletion_status"]

        if exp_status in confusion_matrix and act_status in confusion_matrix[exp_status]:
            confusion_matrix[exp_status][act_status] += 1

        if exp_status == act_status:
            correct_status_count += 1
        else:
            if act_status == "COMPLETE" and exp_status != "COMPLETE":
                false_complete_count += 1
            mismatches.append({
                "case_id": cid,
                "expected": exp_status,
                "actual": act_status,
                "issue": "Status mismatch"
            })

        # Compare steps JSON
        try:
            exp_steps = json.loads(t_row["steps_json"])
            act_steps = json.loads(p_row["steps_json"])
            if exp_steps == act_steps:
                step_exact_matches += 1
        except Exception:
            pass

    status_accuracy = correct_status_count / total_cases if total_cases > 0 else 0.0

    # Calculate per-class metrics
    per_class = {}
    for c in classes:
        tp = confusion_matrix[c][c]
        fp = sum(confusion_matrix[o][c] for o in classes if o != c)
        fn = sum(confusion_matrix[c][o] for o in classes if o != c)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 1.0
        per_class[c] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": sum(confusion_matrix[c].values())
        }

    report = {
        "total_cases": total_cases,
        "correct_status": correct_status_count,
        "status_accuracy": round(status_accuracy, 4),
        "false_complete_count": false_complete_count,
        "step_exact_matches": step_exact_matches,
        "confusion_matrix": confusion_matrix,
        "per_class": per_class,
        "mismatches": mismatches
    }

    print("\n" + "=" * 65)
    print(" GHOST TRACER EVALUATION REPORT")
    print("=" * 65)
    print(f" Total Benchmark Cases:   {total_cases}")
    print(f" Status Accuracy:         {status_accuracy * 100:.2f}% ({correct_status_count}/{total_cases})")
    print(f" False-COMPLETE Count:    {false_complete_count} (Safety Critical)")
    print(f" Exact Step Matches:      {step_exact_matches}/{total_cases}")
    print("\n Per-Class Metrics:")
    for c, metrics in per_class.items():
        print(f"  * {c:<15} Precision: {metrics['precision']:.4f} | Recall: {metrics['recall']:.4f} | F1: {metrics['f1']:.4f} (n={metrics['support']})")

    print("\n Confusion Matrix (Rows: Expected, Cols: Actual):")
    print(f"   {'':<16} {'COMPLETE':<10} {'INCOMPLETE':<12} {'NOT_APPLICABLE':<14}")
    for c in classes:
        print(f"   {c:<16} {confusion_matrix[c]['COMPLETE']:<10} {confusion_matrix[c]['INCOMPLETE']:<12} {confusion_matrix[c]['NOT_APPLICABLE']:<14}")

    if mismatches:
        print(f"\n Mismatches ({len(mismatches)}):")
        for m in mismatches[:5]:
            print(f"   - {m['case_id']}: Expected {m['expected']}, got {m['actual']} ({m.get('issue')})")
    else:
        print("\n [✓] All benchmark sample cases matched canonical expectations with ZERO false-COMPLETE errors!")
    print("=" * 65)

    return report

if __name__ == "__main__":
    preds = sys.argv[1] if len(sys.argv) > 1 else "output.csv"
    truth = sys.argv[2] if len(sys.argv) > 2 else "dataset/sample_output.csv"
    evaluate_predictions(preds, truth)
