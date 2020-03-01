from typing import List

from kivy.utils import platform

IS_MOBILE = platform in ['ios', 'android']

if not IS_MOBILE:
    import numpy as np
    from pyaudio import PyAudio, paInt16

RATE = 16000
CHUNK = 4000  # number of audio samples per frame of test_data
DATA_RATE = 400  # sampling rate of signal activity in audio

# morse parameters
SMALLEST_TIME_UNIT = .08  # the unit of time in seconds that other duration will be multiple of
DOT_DURATION_THRESHOLD_SEC = SMALLEST_TIME_UNIT
DASH_DURATION_THRESHOLD_SEC = SMALLEST_TIME_UNIT * 3
LETTER_END_DURATION_THRESHOLD_SEC = SMALLEST_TIME_UNIT * 3
WORD_END_DURATION_THRESHOLD_SEC = SMALLEST_TIME_UNIT * 7

NUM_BITS_PER_SEC = int(RATE / DATA_RATE)
DOT_DURATION_THRESHOLD_BIT = int(DOT_DURATION_THRESHOLD_SEC * NUM_BITS_PER_SEC)
DASH_DURATION_THRESHOLD_BIT = int(DASH_DURATION_THRESHOLD_SEC * NUM_BITS_PER_SEC)
LETTER_END_DURATION_THRESHOLD_BIT = int(LETTER_END_DURATION_THRESHOLD_SEC * NUM_BITS_PER_SEC)
WORD_END_DURATION_THRESHOLD_BIT = int(WORD_END_DURATION_THRESHOLD_SEC * NUM_BITS_PER_SEC)
MAX_INTENSITY = np.log((2**15)**2)

class AutoMorseRecognizer:
    def __init__(self, mic_engine, debug=False, active_threshold=15):
        self.mic_engine = mic_engine
        self.mic_engine.init_stream(sampling_rate=RATE, frame_size=CHUNK)
        self.debug = debug
        self.active_threshold = active_threshold
        self.old_buffer = []

    def set_threshold(self, active_threshold):
        self.active_threshold = active_threshold

    # todo refactor get_intensity() and update() so it is DRY
    def get_intensity_as_percent(self):
        data = self.mic_engine.get_audio_frame()
        intensity = np.log(np.mean(data ** 2)) / MAX_INTENSITY
        print(intensity)
        return intensity

    def update(self):
        data = self.mic_engine.get_audio_frame()
        morse_code, speech_activity = self.translate_audio_to_morse(data)
        return morse_code, speech_activity

    # def get_morse_from_wav_file(self, audio_path):
    #     fs, x = wavfile.read(audio_path)
    #     x = x.astype(float)
    #     self.old_buffer = np.array([])
    #     for i in range(0, len(x)-CHUNK, CHUNK):
    #         data = x[i:i+CHUNK]
    #         morse_code, _ = self.translate_audio_to_morse(data)
    #         if morse_code:
    #             print(''.join(morse_code), end='')

    @property
    def bits_per_frame(self):
        return int(CHUNK / DATA_RATE)

    @property
    def frame_rate(self):
        return float(CHUNK/RATE)

    def translate_audio_to_morse(self, data):
        try:
            speech_activity = self.raw_audio_to_speech_intensity(data)
            print(speech_activity)
            speech_activity_vec = np.concatenate((self.old_buffer, speech_activity))
            morse_code, self.old_buffer = self.activity_to_morse(speech_activity_vec)
        except Exception as e:
            print(repr(e))
            morse_code, speech_activity_vec = [], [0] * self.bits_per_frame
        return morse_code, speech_activity_vec

    def raw_audio_to_speech_intensity(self, data):
        data_reshaped = data.reshape((-1, DATA_RATE))
        intensity = np.log(np.mean(data_reshaped ** 2, axis=1))
        speech_activity = (intensity > self.active_threshold).astype(int)
        if self.debug:
            print(f'max intensity: {max(intensity)}')
            print(f'min intensity: {min(intensity)}')
        return speech_activity

    def activity_to_morse(self, active_vec):
        morse: List[str] = []
        # vector of indices where the signal went from 1/0 to 0/1
        onoffset_indices = np.concatenate(([0], np.where(np.diff(active_vec) != 0)[0]+1))
        # a vector of len of segment between on/offset
        segment_durations = np.diff(onoffset_indices)
        is_active_vec = active_vec[onoffset_indices]

        # for each segment of consecutive test_data value
        # if the segment exceeds the duration threshold set morse value
        for seg_dur, is_active in zip(segment_durations, is_active_vec):
            if is_active:
                if seg_dur >= DASH_DURATION_THRESHOLD_BIT:
                    morse.append('-')
                else:
                    morse.append('.')
            else:
                if seg_dur >= WORD_END_DURATION_THRESHOLD_BIT:
                    morse.append(' / ')
                elif seg_dur >= LETTER_END_DURATION_THRESHOLD_BIT:
                    morse.append(' ')
        # keep the last segment to be stitched to the next frame
        old_buffer = active_vec[onoffset_indices[-1]:]
        trunc_len = min(len(old_buffer), WORD_END_DURATION_THRESHOLD_BIT)
        old_buffer = old_buffer[-trunc_len:]

        if self.debug:
            print('speech activity vec: ' + str(active_vec))
            print('onoffset_indices: ' + str(onoffset_indices))
            print('segment_durations: ' + str(segment_durations))
            print('old buffer: ' + str(old_buffer))

        return morse, old_buffer


