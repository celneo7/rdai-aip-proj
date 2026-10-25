from faster_whisper import WhisperModel

asr_model = WhisperModel("base", device="cpu", compute_type="int8")