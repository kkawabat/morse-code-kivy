from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.navigationdrawer import NavigationLayout, MDNavigationDrawer
from kivymd.uix.toolbar import MDToolbar

KV = '''
#:import IconLeftWidget kivymd.uix.list.IconLeftWidget
#:import images_path kivymd.images_path


<NavigationItem>
    theme_text_color: 'Custom'
    divider: None

    IconLeftWidget:
        icon: root.icon


<ContentNavigationDrawer>

    BoxLayout:
        orientation: 'vertical'

        FloatLayout:
            size_hint_y: None
            height: "200dp"

            canvas:
                Color:
                    rgba: app.theme_cls.primary_color
                Rectangle:
                    pos: self.pos
                    size: self.size

            BoxLayout:
                id: top_box
                size_hint_y: None
                height: "200dp"
                #padding: "10dp"
                x: root.parent.x
                pos_hint: {"top": 1}

                FitImage:
                    source: f"{images_path}kivymd_alpha.png"

            MDIconButton:
                icon: "close"
                x: root.parent.x + dp(10)
                pos_hint: {"top": 1}
                on_release: root.parent.toggle_nav_drawer()

            MDLabel:
                markup: True
                text: "[b]KivyMD[/b]\\nVersion: 0.102.1"
                #pos_hint: {'center_y': .5}
                x: root.parent.x + dp(10)
                y: root.height - top_box.height + dp(10)
                size_hint_y: None
                height: self.texture_size[1]

        ScrollView:
            pos_hint: {"top": 1}

            GridLayout:
                id: box_item
                cols: 1
                size_hint_y: None
                height: self.minimum_height
'''
Builder.load_string(KV)


class ContentNavigationDrawer(MDNavigationDrawer):
    def __init__(self, nav_layout):
        super(ContentNavigationDrawer, self).__init__()
        self.nav_layout = nav_layout
        self.use_logo = 'logo'
        self.drawer_logo = 'ui/img/nav_drawer_logo.png'
        self.home = NavigationItem(text="Home", icon='home',
                                   on_press=lambda x:
                                   self.change_screen('welcome', self.home))
        self.encode = NavigationItem(text="Encode", icon='database-import',
                                     on_press=lambda x:
                                     self.change_screen('encode', self.encode))
        self.decode = NavigationItem(text="Decode", icon='database-export',
                                     on_press=lambda x:
                                     self.change_screen('decode', self.decode))
        self.message = NavigationItem(text="Messages", icon='message',
                                      on_press=lambda x:
                                      self.change_screen('message', self.message))
        self.training = NavigationItem(text="Training", icon='dumbbell',
                                       on_press=lambda x:
                                       self.change_screen('training', self.training))
        self.add_widget(self.home)
        self.add_widget(self.encode)
        self.add_widget(self.decode)
        self.add_widget(self.message)
        self.add_widget(self.training)

    def change_screen(self, screen, nav_item):
        self.nav_layout.toggle_nav_drawer()
        # I have to manually reset the color back to white
        # because it's not doing it on its own
        nav_item.theme_text_color = [1, 1, 1, 1]
        App.get_running_app().root.content.current = screen


class NavigationItem(OneLineAvatarListItem):
    icon = StringProperty()


class MyNavigationLayout(NavigationLayout):
    def __init__(self, scroll_view=None, **kwargs):
        super(MyNavigationLayout, self).__init__(**kwargs)
        self.content_nav_drawer = ContentNavigationDrawer(self)
        self.drawer_open = False
        self.scroll_view = scroll_view

        self.add_widget(self.content_nav_drawer)
        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.toolbar = MDToolbar()
        self.toolbar.anchor_title = 'center'
        self.toolbar.elevation = 0
        self.toolbar.theme_text_color = 'Custom'
        self.toolbar.text_color = [1, 1, 1, 1]
        self.toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        self.toolbar.left_action_items = [['menu', lambda x: self.toggle_nav_drawer()]]
        toolbar_anchor.add_widget(self.toolbar)
        self.add_widget(toolbar_anchor)

        # This is here because on scroll views the buttons behind the nav bar
        # will count as being pressed instead of the nav drawer buttons
        if self.scroll_view:
            Clock.schedule_interval(self.disable_scroll_buttons, 0.1)

    def disable_scroll_buttons(self, dt):
        if self.state == 'open':
            self.scroll_view.disabled = True
        else:
            self.scroll_view.disabled = False
