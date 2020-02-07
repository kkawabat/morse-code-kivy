from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen

Builder.load_file(r'ui\screens\default_screen.kv')


class DefaultScreen(Screen):
    texture = ObjectProperty(None)
    tex_coords = ListProperty([0, 0, 1, 0, 1, 1, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.texture_init, 0)

    def texture_init(self, *args):
        self.canvas.before.children[-1].texture.wrap = 'repeat'

    def on_enter(self, *args):
        Clock.schedule_interval(self.scroll_texture, 1 / 60.)

    def on_leave(self, *args):
        Clock.unschedule(self.scroll_texture, 1 / 60.)

    def scroll_texture(self, dt):
        for i in range(0, 8, 2):
            self.tex_coords[i] += dt / 3.
