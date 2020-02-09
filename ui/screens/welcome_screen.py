from kivy.lang import Builder

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\welcome_screen.kv')


class WelcomeScreen(DefaultScreen):
    pass
