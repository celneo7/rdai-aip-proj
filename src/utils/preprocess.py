import av 
import numpy as np

def preprocess(audio_data):
    chunks = []
    with av.open(audio_data) as container:
        # get the audio stream
        audio_stream = container.streams.audio[0]

        # print("Sample rate:", audio_stream.codec_context.sample_rate)
        # print("Channel layout:", audio_stream.codec_context.layout.name)


        # configure the output audio format expected by creating resampler
        resampler = av.AudioResampler(
            format="fltp",  # 32-bit floating-point samples, stored separately per channel
            layout="mono", # One channel, combining the source channels if needed
            rate=16000,    # 16,000 samples represent one second of audio
        )

        # decode the compressed audio into frames.
        # each frame contains a small chunk of audio samples
        for frame in container.decode(audio_stream):

            # convert this chunk to the relevant format 
            # Returns a list of output frames: possibly zero, one, or several, because the resampler can buffer samples internally.
            for converted_frame in resampler.resample(frame):

                # convert the audio frame into a NumPy array of numeric samples.
                # For mono "fltp", its shape is (1, number_of_samples).
                samples = converted_frame.to_ndarray()

                # Remove the single-channel dimension:
                # (1, number_of_samples) → (number_of_samples,)
                # Save this chunk so we can join all chunks afterward.
                chunks.append(samples.reshape(-1))

        # Tell the resampler there is no more input.
        # Retrieve any remaining samples held in its internal buffer.
        for converted_frame in resampler.resample(None):
            samples = converted_frame.to_ndarray()
            chunks.append(samples.reshape(-1))

        # Join all the chunks into a single array of samples.
        # Join all chunks into one continuous, one-dimensional waveform.
        waveform = np.concatenate(chunks).astype(np.float32, copy=False)

        # print("Shape:", waveform.shape)
        # print("Data type:", waveform.dtype)
        # print("Duration:", len(waveform) / 16000, "seconds")

        return waveform



if __name__ == "__main__":
    from src.db.database import get_audio

    audio_data = get_audio("jfk.flac")

    if audio_data is None:
        print("Example not found")
    else:
        try:
            preprocess(audio_data)
        finally:
            audio_data.close()