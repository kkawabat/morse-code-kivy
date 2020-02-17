from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from ui.screens.default_screen import DefaultScreen


Builder.load_file(r'ui\screens\encoder_screen.kv')


class EncoderScreen(DefaultScreen):
    def __init__(self, **kwargs):
        super().__init__(title='Text To Morse Code', **kwargs)
        self.util = App.get_running_app().util
        # self.morse_player = self.util.mrose_player
        self.cur_sound_index = 0
        self.sound_list = []
        self.cur_sound = None

    def icon_callbacks(self, text_input, text_btn):
        if text_btn.icon == 'send':
            self.play_prompt(text_input.text)
        elif text_btn.icon == 'close-circle':
            self.clear_input()

    def display_text_as_morse(self, text):
        prompt_as_morse = self.util.morse_helper.text_to_morse(text)
        self.encode_output_label.text = f'{text} as morse: {prompt_as_morse}'

    def clear_input(self):
        self.encode_input.text = ''
        self.encode_output_label.text = ''
        self.clear_sound()

    def play_prompt(self, text):
        self.clear_input()
        if self.cur_sound:
            self.cur_sound_index = 999999
            self.cur_sound.stop()
        print(f"playing morse for: {text}")
        self.display_text_as_morse(text)
        self.init_morse_sounds(text)

    def clear_sound(self):
        if self.cur_sound:
            self.cur_sound.stop()
        self.cur_sound_index = 0
        self.sound_list = []
        self.cur_sound = None

    def init_morse_sounds(self, text):
        for letter in text:
            if letter == ' ':
                self.sound_list.append('long_pause')
            else:
                self.sound_list.append(letter)
                self.sound_list.append('short_pause')

        if len(self.sound_list) > self.cur_sound_index:
            letter_to_play = self.sound_list[self.cur_sound_index]
            self.cur_sound = self.util.morse_helper.get_letter_as_morse_sound(letter_to_play)
            self.cur_sound.bind(on_stop=self.play_next_sound)
            self.cur_sound.play()

    def play_next_sound(self, dt):
        self.cur_sound_index += 1
        if len(self.sound_list) > self.cur_sound_index:
            letter_to_play = self.sound_list[self.cur_sound_index]
            self.cur_sound = self.util.morse_helper.get_letter_as_morse_sound(letter_to_play)
            self.cur_sound.bind(on_stop=self.play_next_sound)
            self.cur_sound.play()

    def return_home(self):
        self.manager.current = 'home'
