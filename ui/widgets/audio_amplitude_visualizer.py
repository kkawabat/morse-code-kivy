from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.card import MDCard

Builder.load_file(r'ui\widgets\audio_amplitude_visualizer.kv')


class AudAmpVisualizer(BoxLayout):

    def __init__(self, init_threshold=10, stack_count=30, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.stack_count = stack_count
        self.pause_color = [1, 1, 0]
        self.beep_color = [1, 0, 0]

        # Builds a stack of rectangle box layouts
        self.cell_array = [MDCard() for _ in range(self.stack_count)]
        for cell in self.cell_array:
            self.add_widget(cell)

        self.threshold = init_threshold
        self.set_threshold(init_threshold)
        self.set_level(0)

    def set_level(self, level):
        activity_level = round(level * self.stack_count)
        for i, current_cell in enumerate(self.cell_array):
            if activity_level <= i:
                current_cell.md_bg_color = current_cell.md_bg_color[:-1] + [0.2]
            else:
                current_cell.md_bg_color = current_cell.md_bg_color[:-1] + [0.8]

    def set_threshold(self, level):
        stack_thresh = round(level * self.stack_count / 100)
        for i, current_cell in enumerate(self.cell_array):
            if stack_thresh <= i:
                current_cell.md_bg_color = self.pause_color + [current_cell.md_bg_color[-1]]
            else:
                current_cell.md_bg_color = self.beep_color + [current_cell.md_bg_color[-1]]

