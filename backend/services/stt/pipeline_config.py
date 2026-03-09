"""STT pipeline configuration.

Goal: keep environment-driven constants separate from the main pipeline implementation
so lifecycle logic and pipeline logic can evolve independently.
"""

from __future__ import annotations

import os


class PipelineConfig:
    """Pipeline configuration sourced from environment variables."""

    # Summary
    SUMMARY_INTERVAL = float(os.getenv("SUMMARY_INTERVAL", "60.0"))
    TICK_INTERVAL = float(os.getenv("TICK_INTERVAL", "10.0"))
    MIN_CHARS_FOR_SUMMARY = int(os.getenv("MIN_CHARS_FOR_SUMMARY", "40"))

    # Memory / buffering
    MAX_AUDIO_BUFFER_SIZE = int(
        os.getenv("MAX_AUDIO_BUFFER_SIZE", str(100 * 1024 * 1024))
    )  # 100MB
    MAX_PARAGRAPH_COUNT = int(os.getenv("MAX_PARAGRAPH_COUNT", "1000"))
    AUDIO_SAVE_INTERVAL = int(os.getenv("AUDIO_SAVE_INTERVAL", "600"))  # 10 minutes

    # Session timeout
    SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "60"))  # 1 minute

    # Retry
    MAX_RETRIES = int(os.getenv("REDIS_MAX_RETRIES", "3"))
    RETRY_DELAY = float(os.getenv("REDIS_RETRY_DELAY", "0.5"))
