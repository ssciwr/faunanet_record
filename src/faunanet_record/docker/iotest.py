import pyaudio
import time
import wave 


for s in range(1, 11, 1):
    sample_rate = 48000
    channels = 1
    input_device_index = 0
    length_in_s = 12.0
    chunk_size = 1024 * s

    print(f"Chunk size: {s}")

    pa = pyaudio.PyAudio() 
    stream = pa.open(
                format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input_device_index=input_device_index,
                input=True,
                start=True,
                frames_per_buffer=chunk_size,
            )

    for i in range(0, 10):
        print(f"Recording {i}")
        frames = b"".join(
                [
                    stream.read(chunk_size)
                    for _ in range(
                        0, int((sample_rate * length_in_s) / chunk_size)
                    )
                ]
            )

        start = time.time()
        with wave.open(f"test_{i}.wav", "wb") as wavfile:

            wavfile.setnchannels(channels)

            wavfile.setsampwidth(pa.get_sample_size(pyaudio.paInt16))

            wavfile.setframerate(sample_rate)

            wavfile.writeframes(frames)
        stop = time.time()

        print(f"Time to write: {stop - start}")
    pa.terminate()