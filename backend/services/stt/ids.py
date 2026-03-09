"""Small helper utilities for session identifiers."""

from __future__ import annotations

import time


def short_sid() -> str:
    """Generate a small-range unique ID compatible with recording_sessions.id (INTEGER).

    Returns:
        9-digit numeric string derived from the millisecond timestamp modulo 1e9.

    Notes:
        - Keeps within INT4 range (<= 999,999,999)
        - Collision probability is extremely low for typical usage
    """

    timestamp_ms = int(time.time() * 1000)
    sid = timestamp_ms % 1_000_000_000
    return str(sid)
