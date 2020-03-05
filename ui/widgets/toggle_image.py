from kivy.properties import StringProperty
from kivy.uix.image import Image


class ToggleImage(Image):
    """widgets that toggles between two images based on on_release"""
    source_on = StringProperty('')
    source_off = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.toggled = False

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.toggled = not self.toggled
            if self.toggled:
                self.source = self.source_off
            else:
                self.source = self.source_on
