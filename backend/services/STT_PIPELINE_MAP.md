# STT pipeline module map (backend)

This is a lightweight orientation doc for the real-time STT pipeline.

## Entry points

- `backend/app/main.py`
  - Creates one `STTPipeline` per WebSocket connection (`/ws/stt` endpoint).
  - Tracks active sessions in memory.

## Core pipeline

- `backend/services/stt_pipeline.py` (`STTPipeline`)
  - Session lifecycle: begin/feed/end.
  - Buffers audio, runs VAD + STT, publishes segments.
  - Periodic summarization loop.
  - Timeout + periodic audio save.

## Redis key conventions

- `backend/services/stt_keys.py`
  - `date_prefix()` → date-based namespace: `stt:YYYY-MM-DD`
  - `build_keys(prefix, sid)` → consistent keys for:
    - `meta`: `{prefix}:meta:{sid}`
    - `segments`: `{prefix}:{sid}:segments`
    - `summaries`: `{prefix}:{sid}:summaries`

## Publish/consume helpers

- `backend/app/util/redis_publisher.py`
  - `init_session_meta`, `publish_segment`, `publish_summary`, `end_session_meta`

- `backend/app/tasks/redis_to_pg.py`
  - Uses `build_keys()` to read Redis lists and persist them into PostgreSQL.

## ML components (used by the pipeline)

- STT
  - `backend/ml/stt_model.py` (`STTModel`)

- VAD
  - `backend/ml/vad.py` (`VADFilter`)

- Post-process
  - `backend/ml/postprocess/silence_segmenter.py` (`SilenceSegmenter`)
  - `backend/ml/postprocess/timestamp_deduplicator.py` (`TimestampDeduplicator`)

- Preprocess
  - `backend/ml/preprocessing/realtime_cleaner.py` (`RealtimeCleaner`)
  - `backend/ml/preprocessing/typo_corrector.py`

## Downstream tasks

- Final summary
  - `backend/app/tasks/final_summary.py`

- Embeddings
  - `backend/app/tasks/embedding_task.py`

- Diarization
  - `backend/services/diarization.py`

## Notes / next small steps

- Add a minimal test harness for `stt_keys.py` (pure functions, easy to test).
- Consider isolating pipeline configuration (`PipelineConfig`) into a dedicated module as it grows.
