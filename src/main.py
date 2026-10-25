from fastapi import FastAPI, HTTPException
from src.model import transcribe_audio
import os 

app = FastAPI(title="Audio Transcription with Whisper")


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}


@app.get("/examples")
def list_examples():
    folder_path = "data/examples"
    files = [f for f in os.listdir(folder_path) if f.endswith((".flac", ".mp3", ".wav"))]

    audio_meta = [
        {
            "id": i,
            "file_name": audio_file,
        }
        for i, audio_file in enumerate(files)
    ]
    return {"audio_files": audio_meta}


@app.post("/transcribe-example")
def transcribe_example(number: int):
    folder_path = "data/examples"
    audio_files = [f for f in os.listdir(folder_path) if f.endswith((".flac", ".mp3", ".wav"))]

    if number < 0 or number >= len(audio_files):
        raise HTTPException(status_code=400, detail=f"Invalid number. Please provide a number between 0 and {len(audio_files) - 1}.")

    audio_file = audio_files[number]
    file_path = os.path.join(folder_path, audio_file)

    metadata = transcribe_audio(file_path)

    return {"audio_file": audio_file, "metadata": metadata}

