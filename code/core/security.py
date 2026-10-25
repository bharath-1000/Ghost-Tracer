"""
Security, integrity, and privacy safeguards for GHOST TRACER.
Includes SHA-256 dataset immutability verification, run manifests,
HMAC identifier pseudonymization, and tamper detection.
"""

import os
import json
import hashlib
import hmac
from typing import Dict, Any, List

PSEUDONYM_KEY = os.environ.get("PSEUDONYM_KEY", "ghost-tracer-default-pseudonym-key").encode("utf-8")

def hash_file_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def pseudonymize_identifier(identifier: str) -> str:
    """Produces a secure one-way HMAC token for logs to avoid leaking raw PII."""
    if not identifier:
        return ""
    mac = hmac.new(PSEUDONYM_KEY, identifier.strip().lower().encode("utf-8"), hashlib.sha256)
    return f"anon_{mac.hexdigest()[:12]}"

class SecurityAuditor:
    @staticmethod
    def snapshot_dataset_hashes(dataset_dir: str = "dataset") -> Dict[str, str]:
        hashes = {}
        for root, _, files in os.walk(dataset_dir):
            for file in sorted(files):
                if file.endswith(".csv") or file.endswith(".db"):
                    p = os.path.join(root, file)
                    rel = os.path.relpath(p, dataset_dir)
                    hashes[rel] = hash_file_sha256(p)
        return hashes

    @staticmethod
    def verify_dataset_integrity(initial_hashes: Dict[str, str], dataset_dir: str = "dataset") -> bool:
        current = SecurityAuditor.snapshot_dataset_hashes(dataset_dir)
        return current == initial_hashes

    @staticmethod
    def generate_run_manifest(output_file: str = "output.csv", dataset_dir: str = "dataset", run_id: str = "run_001") -> Dict[str, Any]:
        manifest = {
            "run_id": run_id,
            "engine_version": "1.0.0-antigravity",
            "output_sha256": hash_file_sha256(output_file) if os.path.exists(output_file) else None,
            "dataset_hashes": SecurityAuditor.snapshot_dataset_hashes(dataset_dir)
        }
        with open("run_manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        return manifest
