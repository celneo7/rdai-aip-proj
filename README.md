# Audio Transcription

A small ASR project using FastAPI and faster-whisper. Choose an example recording or upload your own file to get a transcript, detected language, and timestamps.

Uses Whisper `base` on CPU with INT8. Audio is decoded with PyAV and converted to mono, 16 kHz, float32 samples before transcription. Example recordings are stored as BLOBs in SQLite; custom uploads aren't saved to the database.

## Run with Docker

With Docker running, execute these commands from the project root:

```powershell
docker build -t rdai-aip .
docker run --rm -p 8000:8000 rdai-aip
```

Open http://localhost:8000 for the frontend, or http://localhost:8000/docs to try the API directly.

Examples from `data/examples/` are seeded during the build. Rebuild the image after adding new examples. The model downloads on first startup, so internet access is needed. Removing the container also removes its downloaded model cache.

## Uploads

Supported extensions: `.wav`, `.mp3`, `.flac`, `.m4a`, `.mp4`. Upload limit: 25 MiB. For MP4 files, only the audio is transcribed.

Sample recordings: [faster-whisper test audio](https://github.com/SYSTRAN/faster-whisper/tree/master/tests/data).
