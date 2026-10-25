from src.model import asr_model, transcribe_audio

import os 

folder_path = "data/examples"

for audio in os.listdir(folder_path):
    file_path = os.path.join(folder_path, audio)
    if audio.endswith(".flac") or audio.endswith(".mp3") or audio.endswith(".wav"):

        metadata = transcribe_audio(file_path)

        print(f"{audio}: {metadata} \n")