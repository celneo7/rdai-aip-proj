from src.db.database import init_db, insert_audio_file, file_exists
import os

def seed_examples():
    init_db()

    folder_path = 'data/examples' 
    for file in os.listdir(folder_path):
        
        if file.lower().endswith((".wav", ".mp3", ".flac", ".m4a", ".mp4")) and not file_exists(file):
            file_path = os.path.join(folder_path, file)

            print(f"Seeding audio file: {file_path}")
            with open(file_path, "rb") as audio_file:
                # read audio file
                audio_data = audio_file.read()
        
            insert_audio_file(file, audio_data)
            print(f"Inserted {file} into the database.")

if __name__ == "__main__":
    seed_examples()