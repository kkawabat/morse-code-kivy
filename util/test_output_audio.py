import time

import numpy as np
import pyaudio
import threading

RATE = 16000
p = pyaudio.PyAudio()


def gen_morse_signal_template(frequency, morse_time_unit):
    morse_time_sample = int(RATE * morse_time_unit)

    dot_signal = np.sin(frequency * 2 * np.pi * np.arange(morse_time_sample) / RATE)
    dot_signal[:100] = dot_signal[:100] * np.linspace(0, 1, 100)
    dot_signal[-100:] = dot_signal[-100:] * np.linspace(1, 0, 100)
    dot_signal = dot_signal.astype(np.float32).tostring()

    dash_signal = np.sin(frequency * 2 * np.pi * np.arange(morse_time_sample * 3) / RATE)
    dash_signal[:100] = dash_signal[:100] * np.linspace(0, 1, 100)
    dash_signal[-100:] = dash_signal[-100:] * np.linspace(1, 0, 100)
    dash_signal = dash_signal.astype(np.float32).tostring()

    short_pause = np.zeros(morse_time_sample)
    mid_pause = np.zeros(morse_time_sample * 3)
    long_pause = np.zeros(morse_time_sample * 7)
    return dot_signal, dash_signal, short_pause, mid_pause, long_pause


def play_morse(morse_signals, stop):
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE,
                    frames_per_buffer=1024, output=True, output_device_index=-1)
    for signal in morse_signals:
        stream.write(signal)
        if stop():
            break
    stream.stop_stream()


if __name__ == "__main__":
    dot_signal, dash_signal, short_pause, mid_pause, long_pause = gen_morse_signal_template(200, 0.08)

    signal_ = [dot_signal, short_pause, dot_signal, short_pause,
               dot_signal, short_pause, dot_signal, short_pause,
               dash_signal, short_pause, dash_signal]

    stop_audio = False
    play_sound_thread = threading.Thread(target=play_morse, args=(signal_, lambda: stop_audio))
    play_sound_thread.start()
    stop_audio = True
