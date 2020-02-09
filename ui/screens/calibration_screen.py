# Kivy imports
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget

# kivymd imports
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.slider import Slider

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\calibration_screen.kv')


class CalibrationScreen(DefaultScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.util = App.get_running_app().util

    def on_value_change(self, value):
        self.util.calibration = value
        print(value)

    def change_screen(self, screen):
        self.manager.current = screen
