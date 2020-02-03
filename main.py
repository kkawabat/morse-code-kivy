# qpy:kivy
# Kivy Imports
import gc

from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import ScreenManager
from kivymd.theming import ThemeManager

from ui.screens.calibration_screen import CalibrationScreen
from ui.screens.decoder_screen import DecoderScreen
from ui.screens.encoder_screen import EncoderScreen
from ui.screens.listening_training_screen import ListeningScreen
from ui.screens.tapping_training_screen import TappingScreen
# Project imports
from ui.screens.training_menu_screen import TrainingMenuScreen
from ui.screens.welcome_screen import WelcomeScreen
from util.utility import Utility

gc.disable()


class MainBox(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')
        self.util = kwargs.get('util')
        self.content = ScreenManager()
        self.content.transition = NoTransition()

        self.content.add_widget(WelcomeScreen(name='welcome', util=self.util))
        self.content.add_widget(EncoderScreen(name='encode', util=self.util))
        self.content.add_widget(DecoderScreen(name='decode', util=self.util))
        self.content.add_widget(TrainingMenuScreen(name='training', util=self.util))
        self.content.add_widget(ListeningScreen(name='listening', util=self.util))
        self.content.add_widget(TappingScreen(name='tapping', util=self.util))
        self.content.add_widget(CalibrationScreen(name='calibration', util=self.util))

        self.screens.add_widget(self.content)
        self.add_widget(self.screens)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.primary_hue = '300'
        self.theme_cls.accent_palette = 'Gray'
        self.theme_cls.accent_hue = '800'
        self.theme_cls.theme_style = 'Dark'
        self.accent_color = [255 / 255, 64 / 255, 129 / 255, 1]
        self.util = Utility()
        super().__init__(**kwargs)

    def build(self):
        return MainBox(util=self.util)

    def on_start(self):
        pass
        # self.nav_bar = MyNavigationLayout()
        # self.nav_bar.toolbar.text_color = App.get_running_app().theme_cls.primary_color
        # self.nav_bar.toolbar.md_bg_color = 0, 0, 0, 0
        # self.nav_bar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        # self.nav_bar_anchor.add_widget(self.nav_bar)
        # self.add_widget(self.nav_bar_anchor)


if __name__ == "__main__":
    MainApp().run()
