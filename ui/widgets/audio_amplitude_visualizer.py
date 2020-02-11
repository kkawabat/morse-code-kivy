from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.app import App

from kivymd.uix.card import MDCard


class AudAmpVisualizer(BoxLayout):
    def __init__(self, stack_height=10, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.stack_height = stack_height
        self.off_color = [0, 0, 0, 0]
        self.on_color = App.get_running_app().theme_cls.primary_color

        # Builds a stack of rectangle box layouts
        self.rect_array = [MDCard(size_hint=(1, 1), md_bg_color=self.off_color) for i in range(self.stack_height)]
        for i in self.rect_array:
            self.add_widget(i)

    def set_level(self, level):
        for i, current_cell in enumerate(self.rect_array):
            current_cell.md_bg_color = self.on_color if level < i else self.off_color

