from __future__ import annotations

from datetime import datetime

import backend.services.stt_keys as stt_keys


def test_date_prefix_format(monkeypatch):
    class _FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):  # noqa: ARG003 - signature compat
            return cls(2026, 3, 9, 9, 59, 0)

    monkeypatch.setattr(stt_keys, "datetime", _FixedDateTime)

    assert stt_keys.date_prefix() == "stt:2026-03-09"


def test_build_keys_convention():
    prefix = "stt:2026-03-09"
    sid = "abc123"

    keys = stt_keys.build_keys(prefix=prefix, sid=sid)

    assert keys == {
        "meta": "stt:2026-03-09:meta:abc123",
        "segments": "stt:2026-03-09:abc123:segments",
        "summaries": "stt:2026-03-09:abc123:summaries",
    }
