# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import platform

# kivymd imports
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRound

# project imports
# from ui.widgets.audio_indicator import AudioIndicator
# from ui.widgets.nav_drawer import MyNavigationLayout


class DecoderScreen(Screen):
    def __init__(self, **kwargs):
        super(DecoderScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        if platform not in ['ios', 'android']:
            self.amr = self.util.auto_morse_recognizer
        self.ui_layout()

    def ui_layout(self):
        record_button_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom',
                                            padding=[dp(25), dp(25), dp(25), dp(25)])

        self.record_button = MDFloatingActionButton(icon='record', size=[dp(56), dp(56)])
        self.record_button.md_bg_color = App.get_running_app().theme_cls.primary_color
        self.record_button.text_color = [1, 1, 1, 1]
        if platform not in ['ios', 'android']:
            self.record_button.bind(on_press=lambda x: self.decode_audio())
        record_button_anchor.add_widget(self.record_button)

        self.decode_input = MDTextFieldRound(pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                             size_hint=(0.85, 0.5))
        self.decode_input.icon_left_dasabled = True
        # Moves widget out of the field of view
        self.decode_input.children[2].children[2].pos_hint = {'center_x': 500, 'center_y': 500}
        # This binds the right icon to record the input
        self.decode_input.icon_right = 'database-export'
        self.decode_input.children[2].children[0].bind(on_press=lambda x: self.clear_text())

        decode_card = MDCard(padding=dp(24), spacing=dp(24), orientation='vertical',
                             size_hint_x=0.85, size_hint_y=0.7,
                             pos_hint={'top': 0.85, 'center_x': 0.5})
        decode_label = MDLabel(text='Decode Morse Code Audio', font_style='Body1', halign='center',
                               size_hint=(1, 0.5))
        decode_label.theme_text_color = 'Custom'
        decode_label.text_color = [1, 1, 1, 1]
        decode_card.add_widget(decode_label)

        decode_text = 'Hit record or enter Morse Code below to start decoding'
        self.decode_output_label = MDLabel(text=decode_text, font_style='Body1',
                                           halign='center', size_hint=(1, 0.5))
        self.decode_output_label.theme_text_color = 'Custom'
        self.decode_output_label.text_color = [1, 1, 1, 1]

        decode_card.add_widget(self.decode_output_label)
        decode_card.add_widget(self.decode_input)
        decode_card.md_bg_color = App.get_running_app().theme_cls.accent_color
        decode_card.elevation = 15

        self.add_widget(decode_card)
        self.add_widget(record_button_anchor)

    def clear_text(self):
        self.decode_input.text = ''
        self.decode_output_label.text = ''

    def decode_audio(self):
        if self.record_button.md_bg_color == App.get_running_app().theme_cls.primary_color:
            self.record_button.md_bg_color = App.get_running_app().theme_cls.error_color
            self.decode_output_label.text = ''
            self.amr.start()
            Clock.schedule_interval(self.update_amr, self.amr.frame_rate)

        else:
            self.decode_output_label.text = ''
            self.record_button.md_bg_color = App.get_running_app().theme_cls.primary_color
            Clock.unschedule(self.update_amr)
            self.amr.stop()
            self.clear_text()

    def update_amr(self, kargs):
        morse_code_segment, bit_signal = self.amr.update()
        self.update_morse(morse_code_segment)
        self.update_text_display(self.decode_input.text)

    def update_morse(self, morse_code_segment):
        self.decode_input.text = self.decode_input.text + ''.join(morse_code_segment)

    def update_text_display(self, morse_code):
        user_input = self.util.morse_helper.morse_to_text(morse_code)
        self.decode_output_label.text = user_input

    def return_home(self):
        self.manager.current = 'welcome'
