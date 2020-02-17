# Kivy imports
import random
import time

from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button

from ui.screens.default_screen import DefaultScreen


class LongpressButton(Button):
    __events__ = ('on_long_press', 'on_short_press', 'on_long_pause', 'on_short_pause')

    long_press_dur = Factory.NumericProperty(1)
    short_press_dur = Factory.NumericProperty(1)
    long_pause_dur = Factory.NumericProperty(1)
    short_pause_dur = Factory.NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_release_time = None
        self.last_press_time = None

    def on_release(self):
        self.last_release_time = time.time()
        press_duration = time.time() - self.last_press_time
        if press_duration >= self.long_press_dur:
            self.dispatch('on_long_press')
        else:
            self.dispatch('on_short_press')

    def on_press(self):
        self.last_press_time = time.time()
        if self.last_release_time is not None:
            pause_duration = time.time() - self.last_release_time
            if pause_duration >= self.long_pause_dur:
                print('long_pause')
                self.dispatch('on_long_pause')
            elif pause_duration >= self.short_pause_dur:
                print('short_pause')
                self.dispatch('on_short_pause')

    def set_morse_timing(self, morse_timing_dict):
        self.long_press_dur = morse_timing_dict['long_press_dur']
        self.short_press_dur = morse_timing_dict['short_press_dur']
        self.long_pause_dur = morse_timing_dict['long_pause_dur']
        self.short_pause_dur = morse_timing_dict['short_pause_dur']

    def on_long_press(self, *largs):
        pass

    def on_short_press(self, *largs):
        pass

    def on_long_pause(self, *largs):
        pass

    def on_short_pause(self, *largs):
        pass


Builder.load_file(r'ui\screens\tapping_training_screen.kv')


class TappingScreen(DefaultScreen):
    prompt = StringProperty("")
    decode_morse_text = StringProperty('')
    decode_text = StringProperty('')
    tapping_prompt_text = StringProperty('')
    decode_output_text = StringProperty("^-- click on the left button to clear"
                                        " and the right button for new prompt --^")

    def __init__(self, **kwargs):
        super().__init__(title='Tapping Training', **kwargs)
        self.util = App.get_running_app().util
        self.training_prompt_dict = self.util.training_prompt_dict

    def icon_callbacks(self, text_input, text_btn):
        self.clear_input()
        if text_btn.icon == 'dice-5':
            self.decode_output_text = ""
            if self.util.training_difficulty in ['Easy', 'Medium', 'Hard']:
                if self.util.training_difficulty == 'Easy':
                    training_level = 'letter'
                elif self.util.training_difficulty == 'Medium':
                    training_level = 'word'
                else:
                    training_level = 'sentence'
                self.prompt = random.choice(self.util.training_prompt_dict[training_level])
                self.tapping_prompt_text = f"Please Tap out the {training_level}: {self.prompt}"
            else:
                print(f"failed to load {self.util.training_difficulty}")

    def update_text_display(self):
        self.decode_text = self.util.morse_helper.morse_to_text(self.decode_morse_text)
        if self.prompt == self.decode_text:
            self.decode_output_text = "You got it! click dice icon to do next"

    def update_morse_display(self, morse_code):
        self.decode_morse_text = self.decode_morse_text + ''.join(morse_code)
        self.update_text_display()

    def clear_input(self):
        self.decode_morse_text = ''
        self.decode_text = ''
        self.decode_output_text = ''

    def tapped(self, morse_char):
        print(morse_char)
        self.update_morse_display([morse_char])

    def return_menu(self):
        self.manager.current = 'training'

    def return_home(self):
        self.manager.current = 'home'
