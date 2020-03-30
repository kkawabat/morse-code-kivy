from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\calibration_screen.kv')


class CalibrationScreen(DefaultScreen):
    sensitivity_value_label = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(title='Calibration', **kwargs)
        self.util = App.get_running_app().util
        self.mic_engine = self.util.mic_engine
        default_threshold = self.util.auto_morse_recognizer.active_threshold
        self.sensitivity_value_label = f"{default_threshold:.2f}%"

    def on_slider_value_change(self, slider_value):
        self.util.auto_morse_recognizer.set_threshold(slider_value)
        self.sensitivity_value_label = f"{slider_value:.2f}%"
        self.ids.amp_viz.set_threshold(slider_value)

    def update_amp_viz(self, *args):
        intensity = self.util.auto_morse_recognizer.get_intensity_as_percent()
        self.ids.amp_viz.set_level(intensity)

    def on_enter(self):
        super().on_enter()
        Clock.schedule_interval(self.update_amp_viz, 1 / 10)

    def on_leave(self, *args):
        super().on_leave()
        self.mic_engine.stop_stream()
        Clock.unschedule(self.update_amp_viz)