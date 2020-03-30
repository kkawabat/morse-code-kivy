from kivy.lang import Builder

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\home_screen.kv')


class HomeScreen(DefaultScreen):
    def __init__(self, **kwargs):
        super().__init__(title='Home', **kwargs)
