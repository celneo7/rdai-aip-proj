from pydantic import BaseModel


class AudioRequest(BaseModel):
    filename: str

class TranscriptionResponse(BaseModel):
    filename: str
    metadata: dict


class AudioFilename(BaseModel):
    id: int
    filename: str

class ExamplesResponse(BaseModel):
    audio_files: list[AudioFilename]