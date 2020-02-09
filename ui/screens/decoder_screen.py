# Kivy imports
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from ui.screens.default_screen import DefaultScreen

# kivymd imports
Builder.load_file(r'ui\screens\decoder_screen.kv')


class DecoderScreen(DefaultScreen):
    decode_input_text = StringProperty('')
    decode_output_label_text = StringProperty('Hit record or enter Morse Code below to start decoding')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.util = App.get_running_app().util
        self.amr = self.util.auto_morse_recognizer

    def clear_text(self, *args):
        self.decode_input_text = ''
        self.decode_output_label_text = ''

    def decode_audio(self):
        if self.ids.record_button.md_bg_color == App.get_running_app().theme_cls.primary_color:
            self.ids.record_button.md_bg_color = App.get_running_app().theme_cls.error_color
            self.decode_output_label_text = ''
            self.amr.start()
            Clock.schedule_interval(self.update_amr, self.amr.frame_rate)

        else:
            self.ids.record_button.md_bg_color = App.get_running_app().theme_cls.primary_color
            self.decode_output_label_text = ''
            Clock.unschedule(self.update_amr)
            self.amr.stop()
            self.clear_text()

    def update_amr(self, kargs):
        morse_code_segment, _ = self.amr.update()
        self.decode_input_text = self.decode_input_text + ''.join(morse_code_segment)
        self.decode_output_label_text = self.util.morse_helper.morse_to_text(self.decode_input_text)
        self.ids.decode_input.ids.box.text = 'Finished'

    def return_home(self):
        self.manager.current = 'welcome'
