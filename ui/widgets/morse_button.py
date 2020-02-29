import time

from kivy.properties import DictProperty
from kivy.uix.button import Button


class MorseButton(Button):
    morse_timing_dict = DictProperty(None)
    __events__ = ('on_dash', 'on_dot', 'on_long_pause', 'on_short_pause')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_release_time = None
        self.last_press_time = None

    def on_release(self):
        self.last_release_time = time.time()
        press_duration = time.time() - self.last_press_time
        if press_duration >= self.morse_duration_dict['dash']:
            self.dispatch('on_dash')
        else:
            self.dispatch('on_dot')

    def on_press(self):
        self.last_press_time = time.time()
        if self.last_release_time is not None:
            pause_duration = time.time() - self.last_release_time
            if pause_duration >= self.morse_timing_dict['long_pause']:
                self.dispatch('on_long_pause')
            elif pause_duration >= self.morse_timing_dict['short_pause']:
                self.dispatch('on_short_pause')

    def on_dash(self, *args):
        pass

    def on_dot(self, *args):
        pass

    def on_long_pause(self, *args):
        pass

    def on_short_pause(self, *args):
        pass
