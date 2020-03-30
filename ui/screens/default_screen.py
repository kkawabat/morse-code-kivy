from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen

Builder.load_file(r'ui\screens\default_screen.kv')


class DefaultScreen(Screen):
    texture = ObjectProperty(None)
    tex_coords = ListProperty([0, 0, 1, 0, 1, 1, 0, 1])

    def __init__(self, title='', **kwargs):
        super().__init__(**kwargs)
        self.speed = .001
        self.title = title
        Clock.schedule_once(self.texture_init)

    def texture_init(self, *args):
        self.canvas.before.children[-1].texture.wrap = 'repeat'

    def on_enter(self, *args):
        Clock.schedule_interval(lambda x: self.scroll_texture(), 1 / 30.)

    def on_leave(self, *args):
        Clock.unschedule(self.scroll_texture)

    def scroll_texture(self):
        for i in range(0, 8, 2):
            self.tex_coords[i] = self.tex_coords[i] + self.speed % self.size[0]
