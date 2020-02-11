from kivy.lang import Builder

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\training_menu_screen.kv')


class TrainingMenuScreen(DefaultScreen):
    def __init__(self, **kwargs):
        super().__init__(title='Training Menu', **kwargs)

    def return_home(self):
        self.manager.current = 'home'
