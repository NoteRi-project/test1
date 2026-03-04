"""Small helpers for consistent Redis key naming for the STT pipeline.

Kept in a separate module so the pipeline logic can stay focused on lifecycle.
"""

from __future__ import annotations

from datetime import datetime


def date_prefix() -> str:
    """Date-based namespace (e.g. stt:2025-10-20)."""
    return datetime.now().strftime("stt:%Y-%m-%d")


def build_keys(prefix: str, sid: str) -> dict[str, str]:
    """Generate consistent Redis key names for meta, segments, and summaries.

    Convention: prefix:<suffix>:sid (or prefix:sid:<suffix> for list-like keys)
    """
    return {
        "meta": f"{prefix}:meta:{sid}",
        "segments": f"{prefix}:{sid}:segments",
        "summaries": f"{prefix}:{sid}:summaries",
    }
