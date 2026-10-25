from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.asr_model import transcribe_audio
from src.db.database import file_exists, get_all_audio_filenames, get_audio
from src.model import AudioRequest, ExamplesResponse, TranscriptionResponse
import os

from src.utils.preprocess import preprocess 

app = FastAPI(title="Audio Transcription with Whisper")

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}


@app.get("/examples", response_model=ExamplesResponse)
def list_examples():
    # folder_path = "data/examples"
    # files = [f for f in os.listdir(folder_path) if f.endswith((".flac", ".mp3", ".wav"))]

    # audio_meta = [
    #     {
    #         "id": i,
    #         "file_name": audio_file,
    #     }
    #     for i, audio_file in enumerate(files)
    # ]
    # return {"audio_files": audio_meta}

    return {"audio_files": get_all_audio_filenames()}

@app.post("/transcribe-example")
def transcribe_example(request: AudioRequest):
    # folder_path = "data/examples"
    # audio_files = [f for f in os.listdir(folder_path) if f.endswith((".flac", ".mp3", ".wav"))]

    # if number < 0 or number >= len(audio_files):
    #     raise HTTPException(status_code=400, detail=f"Invalid number. Please provide a number between 0 and {len(audio_files) - 1}.")

    # audio_file = audio_files[number]
    # file_path = os.path.join(folder_path, audio_file)

    file = request.filename
    if not file_exists(file):
        raise HTTPException(status_code=404, detail="Audio File not found")

    audio_data = get_audio(request.filename)

    try:
        waveform = preprocess(audio_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio file: {str(e)}")
    finally:
        audio_data.close()

    metadata = transcribe_audio(waveform)

    return TranscriptionResponse(filename=request.filename, metadata=metadata)


@app.post("/transcribe")
def transcribe_upload(file: UploadFile):
    MAX_UPLOAD_BYTES = 25 * 1024 * 1024

    try:
        # empty file check
        if file.filename == "":
            raise HTTPException(status_code=400, detail="No file uploaded")

        # supported file type check
        if not file.filename.endswith((".flac", ".mp3", ".wav", ".m4a", ".mp4")):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .flac, .mp3, or .wav file.")

        # file size check
        if file.size is not None and file.size > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 25 MB.") 

        waveform = preprocess(file.file)
        metadata = transcribe_audio(waveform)

        return TranscriptionResponse(filename=file.filename, metadata=metadata)
    finally:
        file.file.close()