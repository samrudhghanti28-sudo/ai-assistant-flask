"""feedback_store.py

A very small feedback logging utility used by BOTH CLI and Flask.

Requirement covered:
- After every AI response, ask the user "Was this response helpful? (yes/no)"
- Collect/store the feedback for improvement

Implementation choice:
- Store each interaction as one JSON object per line in a .jsonl file.
  This format is easy to read, append, and analyze later.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


FEEDBACK_FILE = Path(__file__).with_name("feedback_log.jsonl")


def append_feedback(entry: Dict[str, Any]) -> None:
    """Append a feedback record to FEEDBACK_FILE.

    We always add a timestamp so you can see when the feedback was recorded.
    """

    safe_entry = dict(entry)
    safe_entry["timestamp"] = datetime.now().isoformat(timespec="seconds")

    # Ensure parent dir exists (should, but safe)
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

    with FEEDBACK_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(safe_entry, ensure_ascii=False) + "\n")


def read_all_feedback(limit: int = 50) -> list[Dict[str, Any]]:
    """Read last N feedback entries (for display/debug)."""

    if not FEEDBACK_FILE.exists():
        return []

    lines = FEEDBACK_FILE.read_text(encoding="utf-8").splitlines()
    lines = lines[-limit:]

    results: list[Dict[str, Any]] = []
    for line in lines:
        try:
            results.append(json.loads(line))
        except json.JSONDecodeError:
            # Skip corrupted lines
            continue

    return results
