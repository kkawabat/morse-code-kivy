import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                frames_per_buffer=1024,
                output=True,
                output_device_index=1
                )
samples = np.sin(np.arange(50000)/20)
stream.write(samples.astype(np.float32).tostring())
stream.close()