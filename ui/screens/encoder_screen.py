from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from ui.screens.default_screen import DefaultScreen
from kivymd.uix.textfield import MDTextField

Builder.load_file(r'ui\screens\encoder_screen.kv')


class EncoderScreen(DefaultScreen):
    def __init__(self, **kwargs):
        super().__init__(title='Text To Morse Code', **kwargs)
        self.util = App.get_running_app().util

    def icon_callbacks(self, text_input, text_btn):
        if text_btn.icon == 'send':
            self.play_prompt(text_input.text)
        elif text_btn.icon == 'close-circle':
            self.clear_input()

    def display_text_as_morse(self, text):
        prompt_as_morse = self.util.morse_helper.text_to_morse(text)
        self.ids['encode_output_label'].text = f'{text} as morse: {prompt_as_morse}'

    def clear_input(self):
        self.ids['encode_input'].text = ''
        self.ids['encode_output_label'].text = ''
        self.util.morse_helper.clear_sound()

    def play_prompt(self, text):
        print(f"playing morse for: {text}")
        self.display_text_as_morse(text)
        self.util.morse_helper.text_to_morse_sound(text)

    def return_home(self):
        self.manager.current = 'home'
