# Kivy imports
import random
import time

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.textinput import TextInput

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\tapping_speed_test_screen.kv')


class TappingSpeedTestScreen(DefaultScreen):
    decode_morse_text = StringProperty('')
    decode_text = StringProperty('')
    prompt_display = StringProperty('')
    decode_morse2 = ObjectProperty(None)
    morse_button_text = StringProperty('Start Speed Test')

    # tog_img = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(title='Tapping Training', **kwargs)
        self.util = App.get_running_app().util
        self.prompt_text = ""
        self.prompt_display = ""
        self.cur_state = None
        self.reset_test()

    def update_displays(self, morse_code):
        self._decode_morse_text = self._decode_morse_text + ''.join(morse_code)
        self.decode_morse_text = self._decode_morse_text[-100:]
        self._decode_text = self.util.morse_helper.morse_to_text(self._decode_morse_text)
        self.decode_text = self._decode_text[-100:]
        num_correct, _, _, _ = self.calc_correct_position()
        self.prompt_display = f"[color=33ff33]{self.prompt_text[:num_correct]}[/color]{self.prompt_text[num_correct:]}"
        if len(self.prompt_text) == num_correct:
            self.display_score_popup()

    def reset_test(self):
        self._decode_morse_text = ""
        self.decode_morse_text = '[color=222222]Your morse will be displayed here[/color]'
        self._decode_text = ""
        self.decode_text = '[color=222222]Your decoded message will be displayed here[/color]'
        self.prompt_text = ''
        self.prompt_display = "[color=222222]Type the words that appears here when you start the test[/color]"
        self.morse_button_text = "Start Speed Test"
        # self.tog_img.set_toggle(False)
        self.cur_state = 'stopped'

    def start_test(self):
        self.test_start = time.time()
        self.generate_prompt_text()

    def on_enter(self, *args):
        super().on_enter()
        self.reset_test()

    def tapped(self, morse_char):
        print(self.cur_state)
        if self.cur_state == 'stopped':
            self.start_test()
            self.cur_state = "init_press"
        elif self.cur_state == 'init_press':
            self.cur_state = 'started'
        else:
            self.update_displays([morse_char])

    def calc_correct_position(self):
        num_correct = 0
        chain_correct = 0
        tmp_chain_correct = 0
        chain_correct_wo_spaces = 0
        tmp_chain_correct_wo_space = 0
        num_incorrect = 0

        for decoded_char in self._decode_text:
            if self.prompt_text[num_correct] == decoded_char:
                num_correct += 1
                tmp_chain_correct += 1
            else:
                if decoded_char == " ":
                    chain_correct = max(chain_correct, tmp_chain_correct)
                    tmp_chain_correct = 0
                chain_correct_wo_spaces = max(chain_correct_wo_spaces, tmp_chain_correct_wo_space)
                tmp_chain_correct_wo_space = 0
                num_incorrect += 1
        return num_correct, num_incorrect, chain_correct, chain_correct_wo_spaces

    def display_score_popup(self):
        total_time = time.time() - self.test_start
        num_correct, num_incorrect, chain_correct, chain_correct_wo_spaces = self.calc_correct_position()
        num_mistake = len(self.decode_text) - num_correct
        popup_layout = BoxLayout(orientation='Vertical')
        cur_stat_text = TextInput(text=f"Total time: {total_time:.1f} seconds\n"
                                       f"character per second: {num_correct / total_time}\n"
                                       f"Longest correct chain (w/ space): {chain_correct}"
                                       f"Longest correct chain (w/o space): {chain_correct_wo_spaces}\n"
                                       f"number of mistakes: {num_mistake}",
                                  multiline=True, readonly=True)
        score_board = TextInput(text=f"Score Board\n",
                                multiline=True, readonly=True)
        close_btn = Button(text='Close')
        popup_layout.add_widget(cur_stat_text)
        popup_layout.add_widget(close_btn)
        score_popup = Popup(title="Time's up", content=popup_layout, auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        close_btn.bind(on_press=score_popup.dismiss)
        score_popup.open()
        self.reset_test()

    def generate_prompt_text(self):
        self.decode_morse_text = ""
        self.decode_text = ""
        self.prompt_display = ""
        self.prompt_text = ' '.join(random.sample(self.util.training_prompt_dict['word'], 10))
        self.prompt_display = self.prompt_text
        self.morse_button_text = "Tap"

    def return_home(self):
        self.manager.current = 'home'
