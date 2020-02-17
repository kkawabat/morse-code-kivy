import numpy as np
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from pyaudio import paInt16, PyAudio

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\calibration_screen.kv')


class CalibrationScreen(DefaultScreen):
    sensitivity_value_label = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(title='Calibration', **kwargs)
        self.util = App.get_running_app().util
        self.mic_engine = self.util.mic_engine

    def on_slider_value_change(self, slider_value):
        self.util.auto_morse_recognizer.set_threshold(slider_value)
        self.sensitivity_value_label = str(round(slider_value, 2))
        self.ids.amp_viz.set_threshold(slider_value)

    def update_amp_viz(self, *args):
        data = self.mic_engine.get_audio_frame()
        intensity = np.log(np.mean(data ** 2)) * 8
        print(intensity)
        self.ids.amp_viz.set_level(intensity)

    def on_enter(self):
        self.mic_engine.init_stream(sampling_rate=16000, frame_size=800)
        Clock.schedule_interval(self.update_amp_viz, 1 / 20)

    def on_leave(self, *args):
        self.mic_engine.stop_stream()
        Clock.unschedule(self.update_amp_viz)