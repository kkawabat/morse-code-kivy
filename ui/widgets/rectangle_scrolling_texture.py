from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty, ListProperty


class RectScrollingTexture(Rectangle):
    texture = ObjectProperty(None)
    tex_coords = ListProperty([0, 0, 1, 0, 1, 1, 0, 1])

    def __init__(self, **kwargs):
        super(RectScrollingTexture, self).__init__(**kwargs)
        Clock.schedule_once(self.texture_init)
        Clock.schedule_interval(self.scroll_texture, 1 / 30.)

    def texture_init(self, *args):
        self.texture.wrap = 'repeat'

    def scroll_texture(self, dt):
        for i in range(0, 8, 2):
            self.tex_coords[i] += dt / 4.
