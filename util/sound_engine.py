import threading

from pyaudio import PyAudio, paFloat32


class SoundEngine:

    def __init__(self, rate=16000):
        self.pyaudio_engine = PyAudio()
        self.rate = rate
        self.audio_thread = None
        self.stop_audio_flag = False

    def play_audio(self, audio_signals):
        self.stop_audio()
        self.audio_thread = threading.Thread(target=self._play_audio, args=(audio_signals, lambda: self.stop_audio_flag))
        self.stop_audio_flag = False
        self.audio_thread.start()

    def stop_audio(self):
        if self.audio_thread is not None:
            self.stop_audio_flag = True
            while self.audio_thread.is_alive():
                print('wait')
            self.audio_thread = None

    def _play_audio(self, audio_signals, stop):
        stream = self.pyaudio_engine.open(format=paFloat32, channels=1, rate=self.rate,
                                          frames_per_buffer=1024, output=True, output_device_index=-1)
        for signal in audio_signals:
            stream.write(signal)
            if stop():
                break
        stream.stop_stream()

