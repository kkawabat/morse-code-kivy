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
        super().__init__(title='Morse Code Recognizer', **kwargs)
        self.util = App.get_running_app().util
        self.amr = self.util.auto_morse_recognizer
        self.mic_engine = self.util.mic_engine

    def toggle_amr(self):
        self.clear_text()
        if self.ids.record_button.md_bg_color == App.get_running_app().theme_cls.primary_color:
            self.start_amr()
        else:
            self.stop_amr()

    def clear_text(self, *args):
        self.decode_input_text = ''
        self.decode_output_label_text = ''

    def start_amr(self):
        self.ids.record_button.md_bg_color = App.get_running_app().theme_cls.error_color
        self.mic_engine.start_stream()
        Clock.schedule_interval(self.update_amr, self.amr.frame_rate)

    def stop_amr(self):
        self.ids.record_button.md_bg_color = App.get_running_app().theme_cls.primary_color
        self.mic_engine.stop_stream()
        Clock.unschedule(self.update_amr)

    def update_amr(self, kargs):
        data = self.mic_engine.get_audio_frame()
        morse_code_segment, _ = self.amr.translate_audio_to_morse(data)
        self.decode_input_text = self.decode_input_text + ''.join(morse_code_segment)
        self.decode_output_label_text = self.util.morse_helper.morse_to_text(self.decode_input_text)
        self.ids.decode_input.ids.box.text = 'Finished'

    def on_enter(self):
        super().on_enter()
        self.mic_engine.init_stream(sampling_rate=16000, frame_size=4000)

    def on_leave(self):
        super().on_leave()
        self.stop_amr()

    def return_home(self):
        self.manager.current = 'home'
