from fastapi import FastAPI, HTTPException
from src.asr_model import transcribe_audio
from src.db.database import file_exists, get_all_audio_filenames, get_audio
from src.model import AudioRequest, ExamplesResponse, TranscriptionResponse
import os

from src.utils.preprocess import preprocess 

app = FastAPI(title="Audio Transcription with Whisper")


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

