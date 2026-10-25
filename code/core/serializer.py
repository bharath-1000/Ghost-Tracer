"""
Output serialization and formatting for GHOST TRACER.
Ensures deterministic, byte-consistent CSV and JSON rendering.
"""

import csv
import json
from typing import List, Dict, Any

def serialize_steps(steps: List[Dict[str, Any]]) -> str:
    if not steps:
        return "[]"
    # Ensure exact 7 keys in consistent order
    cleaned_steps = []
    for s in steps:
        cleaned_steps.append({
            "step_no": s["step_no"],
            "phase": s["phase"],
            "system_id": s["system_id"],
            "resource_id": s["resource_id"],
            "operation": s["operation"],
            "state": s["state"],
            "evidence_id": s.get("evidence_id", "")
        })
    return json.dumps(cleaned_steps, separators=(',', ':'), ensure_ascii=False)

def write_output_csv(rows: List[Dict[str, Any]], out_path: str = "output.csv"):
    sorted_rows = sorted(rows, key=lambda r: r["case_id"])
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "deletion_status", "steps_json"])
        for r in sorted_rows:
            writer.writerow([r["case_id"], r["deletion_status"], r["steps_json"]])
