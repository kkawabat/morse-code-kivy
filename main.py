from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarListItem

from util.utility import Utility


class ContentNavigationDrawer(BoxLayout):
    pass


class NavigationItem(OneLineAvatarListItem):
    icon = StringProperty()

    def __init__(self, name=None, text=None, icon=None, on_release_func=None, **kwargs):
        self.name = name
        self.text = text
        self.icon = icon
        if on_release_func is None:
            self.on_release = lambda: App.get_running_app().change_screen(self)
        else:
            self.on_release = on_release_func
        super().__init__(**kwargs)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = 'Morse Coder'
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.primary_hue = '300'
        self.theme_cls.accent_palette = 'Gray'
        self.theme_cls.accent_hue = '800'
        self.theme_cls.theme_style = 'Dark'
        self.accent_color = [1, .25, .5, 1]
        self.util = Utility()

    def on_start(self):
        self.init_nav_menu()

    def init_nav_menu(self):
        nav_item_dict = {
            "home": ("home", "Home", None),
            "decode": ("text-to-speech", "Translate Morse Code", None),
            "encode": ("comment-text", "Text to Morse Code", None),
            "training": ("dumbbell", "Training", None),
            "calibration": ("cogs", 'Calibrate', None),
            "exit": ("exit-to-app", "Exit", self.stop)}

        for nav_screen, (nav_icon, nav_text, on_release_func) in nav_item_dict.items():
            nav_item = NavigationItem(name=nav_screen, text=nav_text, icon=nav_icon, on_release_func=on_release_func)
            self.root.ids.content_drawer.ids.box_item.add_widget(nav_item)

    def change_screen(self, nav_item):
        self.root.ids.nav_drawer.toggle_nav_drawer()
        self.root.ids.screen_manager.current = nav_item.name


MainApp().run()
