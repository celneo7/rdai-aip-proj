
import sqlite3
from contextlib import closing
from io import BytesIO

DB_PATH = "./src/db/audio_files.db"

def init_db():
    # create database
    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS audio_files (
                id INTEGER PRIMARY KEY,
                filename TEXT NOT NULL UNIQUE,
                audio_data BLOB NOT NULL
            )
        """)


def insert_audio_file(filename: str, audio_data: bytes):
    # insert audio file into the database
    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            connection.execute(
                "INSERT INTO audio_files (filename, audio_data) VALUES (?, ?)",
                (filename, audio_data),
            )

def get_audio(filename: str):
    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.row_factory = sqlite3.Row

        # get audio data
        row = connection.execute(
            "SELECT audio_data FROM audio_files WHERE filename = ?",
            (filename,),
        ).fetchone()

    
    return BytesIO(row[0]) if row is not None else None


def file_exists(filename: str) -> bool:
    with closing(sqlite3.connect(DB_PATH)) as connection:
        row = connection.execute(
            "SELECT 1 FROM audio_files WHERE filename = ?",
            (filename,),
        ).fetchone()

    return row is not None

def get_all_audio_filenames():
    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            "SELECT id, filename FROM audio_files ORDER BY id"
        ).fetchall()

    return [dict(row) for row in rows]

def delete_audio_file(filename: str):
    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            connection.execute(
                "DELETE FROM audio_files WHERE filename = ?",
                (filename,),
            )

