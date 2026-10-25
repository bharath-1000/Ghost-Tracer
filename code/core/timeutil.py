"""
Temporal correctness utility for GHOST TRACER.
Enforces audit_at boundary cutoffs, UTC normalization, and timestamp comparisons.
"""

from datetime import datetime, timezone
from typing import Optional

def parse_iso_utc(ts_str: Optional[str]) -> Optional[datetime]:
    if not ts_str or not ts_str.strip():
        return None
    s = ts_str.strip()
    # Normalize Z suffix to +00:00 for fromisoformat
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            # Documented assumption: naive timestamps treated as UTC
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None

def is_within_cutoff(ts_str: Optional[str], audit_at_str: Optional[str]) -> bool:
    """
    Checks if ts_str is on or before audit_at (inclusive).
    If audit_at is missing, returns True.
    If ts_str is missing or unparseable, returns False (unverifiable timestamps cannot be decisive).
    """
    if not audit_at_str:
        return True
    dt = parse_iso_utc(ts_str)
    cutoff = parse_iso_utc(audit_at_str)
    if not dt or not cutoff:
        return False
    return dt <= cutoff
