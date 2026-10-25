#!/usr/bin/env python3
"""
GHOST TRACER — Principal CLI and Auditing Entry Point
HackerRank Orchestrate (October 2026): "Ghost Data Still Exists"
"""

import os
import sys
import csv
import argparse
import time

# Ensure code root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.intent import classify_intent
from core.identity import IdentityResolver
from core.policy import PolicyEngine
from core.lifecycle import LifecycleAnalyzer
from core.evidence_scanner import EvidenceScanner
from core.adjudicator import Adjudicator
from core.serializer import serialize_steps, write_output_csv
from core.validator import validate_output_file
from core.security import SecurityAuditor

def audit_case(req: dict, identity_resolver: IdentityResolver, policy_engine: PolicyEngine,
               lifecycle_analyzer: LifecycleAnalyzer, evidence_scanner: EvidenceScanner,
               adjudicator: Adjudicator) -> dict:
    case_id = req["case_id"]
    email = req["email"]
    audit_at = req["audit_at"]
    req_text = req.get("request_text", "")

    # 1. Intent classification
    intent_res = classify_intent(req_text)

    # 2. Identity resolution
    identity = identity_resolver.resolve(email)

    # 3. Evidence scan (up to audit_at)
    scan_res = evidence_scanner.scan_user_evidence(identity, audit_at)

    # 4. Lifecycle recreation risks (up to audit_at)
    risks = lifecycle_analyzer.find_risks(identity["user_id"], audit_at)

    # 5. Adjudication
    adj_res = adjudicator.adjudicate(req, intent_res, identity, scan_res, risks)

    # 6. Serialized steps
    steps_json = serialize_steps(adj_res["steps"])

    return {
        "case_id": case_id,
        "deletion_status": adj_res["deletion_status"],
        "steps_json": steps_json,
        "raw_steps": adj_res["steps"],
        "decision_trace": adj_res["decision_trace"],
        "intent": intent_res,
        "identity": identity,
        "findings_count": adj_res["findings_count"],
        "recreation_risks_count": adj_res["recreation_risks_count"]
    }

def main():
    parser = argparse.ArgumentParser(description="GHOST TRACER — AI-Powered Data Deletion Auditor")
    parser.add_argument("--samples", action="store_true", help="Audit the 32 benchmark sample cases")
    parser.add_argument("--cases", type=str, help="Comma-separated case IDs to audit (e.g. case_001,case_009)")
    parser.add_argument("--limit", type=int, help="Limit number of requests to process")
    parser.add_argument("--explain", type=str, help="Explain decision trace for a specific case_id")
    parser.add_argument("--out", type=str, default="output.csv", help="Path to write output.csv (default: output.csv)")
    parser.add_argument("--debug-trace", action="store_true", help="Print debug decision traces")
    parser.add_argument("--encrypt-artifacts", action="store_true", help="Enable artifact encryption at rest")
    args = parser.parse_args()

    start_time = time.time()
    print("=" * 70)
    print(" GHOST TRACER: Track the Ghost. Prove the Deletion.")
    print(" AI-Powered Deletion Audit Engine — Enterprise Compliance Grade")
    print("=" * 70)

    # Snapshot dataset integrity before run
    initial_hashes = SecurityAuditor.snapshot_dataset_hashes()

    input_file = "dataset/sample_deletion_requests.csv" if args.samples else "dataset/deletion_requests.csv"
    if not os.path.exists(input_file):
        print(f"Error: Target dataset file '{input_file}' not found.")
        sys.exit(1)

    # Load engine components
    print("[1/5] Initializing identity resolution, policy, and evidence engines...")
    identity_resolver = IdentityResolver()
    policy_engine = PolicyEngine()
    lifecycle_analyzer = LifecycleAnalyzer()
    evidence_scanner = EvidenceScanner()
    adjudicator = Adjudicator()

    # Read requests
    requests = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            requests.append(row)

    if args.cases:
        target_ids = set(args.cases.split(","))
        requests = [r for r in requests if r["case_id"] in target_ids]

    if args.limit and args.limit > 0:
        requests = requests[:args.limit]

    print(f"[2/5] Auditing {len(requests)} cases from {input_file}...")
    results = []
    status_counts = {"COMPLETE": 0, "INCOMPLETE": 0, "NOT_APPLICABLE": 0}

    for idx, req in enumerate(requests, start=1):
        res = audit_case(req, identity_resolver, policy_engine, lifecycle_analyzer, evidence_scanner, adjudicator)
        results.append(res)
        status_counts[res["deletion_status"]] += 1

        if args.debug_trace or (args.explain and args.explain == req["case_id"]):
            print(f"\n--- Decision Trace for {req['case_id']} ({res['deletion_status']}) ---")
            for t in res["decision_trace"]:
                print(f"  * {t}")

    # Write output.csv
    print(f"[3/5] Serializing and writing predictions to '{args.out}'...")
    write_output_csv(results, out_path=args.out)

    # Validate contract
    print(f"[4/5] Executing HackerRank contract validation on '{args.out}'...")
    expected_rows = len(requests)
    is_valid, violations = validate_output_file(args.out, expected_count=expected_rows)
    if not is_valid:
        print("\n[!] VALIDATION FAILED! Violations detected:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("  -> Output schema & contract validation: 100% PASSED (0 violations)")

    # Verify dataset immutability
    print("[5/5] Verifying dataset immutability assertion...")
    if not SecurityAuditor.verify_dataset_integrity(initial_hashes):
        print("[!] ERROR: Dataset files were modified during audit execution! Immutability violated.")
        sys.exit(1)
    else:
        print("  -> Dataset immutability verified: SHA-256 hashes matched.")

    # Generate run manifest
    manifest = SecurityAuditor.generate_run_manifest(output_file=args.out)

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f" AUDIT COMPLETE in {elapsed:.2f}s")
    print(f" Cases Audited:        {len(results)}")
    print(f" Complete Deletions:   {status_counts['COMPLETE']}")
    print(f" Incomplete Deletions: {status_counts['INCOMPLETE']}")
    print(f" Not Applicable:       {status_counts['NOT_APPLICABLE']}")
    print(f" Output File:          {args.out}")
    print(f" Manifest Generated:   run_manifest.json (SHA-256: {manifest.get('output_sha256')[:12]}...)")
    print("=" * 70)

if __name__ == "__main__":
    main()
