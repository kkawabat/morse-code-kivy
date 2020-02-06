from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarListItem

from util.utility import Utility


class ContentNavigationDrawer(BoxLayout):
    pass


class NavigationItem(OneLineAvatarListItem):
    icon = StringProperty()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.primary_hue = '300'
        self.theme_cls.accent_palette = 'Gray'
        self.theme_cls.accent_hue = '800'
        self.theme_cls.theme_style = 'Dark'
        self.accent_color = [1, .25, .5, 1]
        self.util = Utility()

    def on_start(self):
        for items in {
            "home-circle-outline": "Home",
            "update": "Check for Update",
            "settings-outline": "Settings",
            "exit-to-app": "Exit",
        }.items():
            self.root.ids.content_drawer.ids.box_item.add_widget(
                NavigationItem(
                    text=items[1],
                    icon=items[0],
                )
            )


MainApp().run()


#
#
#
#
# # qpy:kivy
# # Kivy Imports
# import gc
#
# from kivy.lang import Builder
# from kivy.properties import StringProperty
# from kivy.uix.boxlayout import BoxLayout
# from kivymd.app import MDApp
# from kivymd.uix.list import OneLineAvatarListItem
#
# # Project imports
#
# gc.disable()
#
#
# # class MainBox(FloatLayout):
# #     def __init__(self, **kwargs):
# #         super().__init__()
# #         self.screens = AnchorLayout(anchor_x='center', anchor_y='center')
# #         self.util = kwargs.get('util')
# #         self.content = ScreenManager()
# #         self.content.transition = NoTransition()
# #
# #         self.content.add_widget(WelcomeScreen(name='welcome', util=self.util))
# #         self.content.add_widget(EncoderScreen(name='encode', util=self.util))
# #         self.content.add_widget(DecoderScreen(name='decode', util=self.util))
# #         self.content.add_widget(TrainingMenuScreen(name='training', util=self.util))
# #         self.content.add_widget(ListeningScreen(name='listening', util=self.util))
# #         self.content.add_widget(TappingScreen(name='tapping', util=self.util))
# #         self.content.add_widget(CalibrationScreen(name='calibration', util=self.util))
# #
# #         self.screens.add_widget(self.content)
# #         self.add_widget(self.screens)
#
# class ContentNavigationDrawer(BoxLayout):
#     pass
#
#
# class NavigationItem(OneLineAvatarListItem):
#     icon = StringProperty()
#
#
# class MainApp(MDApp):
#     # def __init__(self, **kwargs):
#     #     self.theme_cls.primary_palette = 'Teal'
#     #     self.theme_cls.primary_hue = '300'
#     #     self.theme_cls.accent_palette = 'Gray'
#     #     self.theme_cls.accent_hue = '800'
#     #     self.theme_cls.theme_style = 'Dark'
#     #     self.accent_color = [1, .25, .5, 1]
#     #     self.util = Utility()
#     #     super().__init__(**kwargs)
#
#     def build(self):
#         return Builder.load_file(r'C:\Users\kkawa\PycharmProjects\morse_code_traininer\main.kv')
#         # return MainBox(util=self.util)
#
#     # def on_start(self):
#     #     pass
#         # self.nav_bar = MyNavigationLayout()
#         # self.nav_bar.toolbar.text_color = App.get_running_app().theme_cls.primary_color
#         # self.nav_bar.toolbar.md_bg_color = 0, 0, 0, 0
#         # self.nav_bar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
#         # self.nav_bar_anchor.add_widget(self.nav_bar)
#         # self.add_widget(self.nav_bar_anchor)
#
#
# if __name__ == "__main__":
#     MainApp().run()
