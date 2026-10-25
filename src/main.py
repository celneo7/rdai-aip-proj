from src.model import asr_model

import os 

folder_path = "data/examples"

for audio in os.listdir(folder_path):
    file_path = os.path.join(folder_path, audio)
    if audio.endswith(".flac") or audio.endswith(".mp3") or audio.endswith(".wav"):

        # Transcribe the audio file using the Whisper model
        segments, info = asr_model.transcribe(file_path)
        print("Transcription complete for file:", audio)

        # Print the segments and detected language
        print("Segments:")
        for segment in segments:
            # Print the start and end times of the segment, along with the transcribed text
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        print(f"Detected language: {info.language}\n")

