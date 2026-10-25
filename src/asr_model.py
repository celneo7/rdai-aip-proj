from importlib.metadata import metadata

from faster_whisper import WhisperModel

asr_model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(audio_data):
    segments, info = asr_model.transcribe(audio_data)

    # extract segments and detected language
    meta_segment = []
    text = ""
    for segment in segments:
        meta_segment.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text
        })
        text += segment.text + " "

    # return the relevant metadata
    metadata = {
        "language": info.language,
        "text": text,
        "segments": meta_segment
    }
    return metadata