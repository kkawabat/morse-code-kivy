from kivy.clock import Clock
from kivy.lang.builder import Builder

from kivymd.uix.button import MDRectangleFlatIconButton

Builder.load_file(r'ui\widgets\default_button.kv')


class DefaultButton(MDRectangleFlatIconButton):
    """Simple buttons"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._init_style)

    def _init_style(self, _):
        """Workaround to access children in this kivymd widget"""
        # Set Label to White
        self.ids.lbl_txt.text_color = [1, 1, 1, 1]
        self.ids.lbl_txt.font_size = 20
        # Set Icon to white
        self.ids.lbl_ic.text_color = [1, 1, 1, 1]
        self.ids.lbl_ic.font_size = 30
