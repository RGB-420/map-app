from kivymd.uix.screen import MDScreen
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarLeadingButtonContainer, MDActionTopAppBarButton
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.button.button import MDButtonText, MDFabButton

from screen.map import Map

class UbiMapScreen(MDScreen):
    def __init__(self, screen_manager,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager = screen_manager
        self.position = [0,0]

        layout = BoxLayout(orientation = 'vertical')

        self.toolbar = MDTopAppBar(type="small")
        return_button = MDTopAppBarLeadingButtonContainer(MDActionTopAppBarButton(icon="arrow-left", on_release=self.back))
        self.toolbar.add_widget(return_button)

        layout.add_widget(self.toolbar)

        content = FloatLayout(size_hint=(1,1))

        self.map_view = Map.build_map(41.3674,2.0567)
        content.add_widget(self.map_view)

        self.center_pin = Image(source="images\marker.png", size_hint=(0.1, 0.1))
        self.update_pin_position()
        
        content.add_widget(self.center_pin)

        self.accept_button = MDFabButton(icon="check", pos_hint= {"center_x": 0.5, "center_y": 0.2}, on_release=self.accept)
        content.add_widget(self.accept_button)

        layout.add_widget(content)

        self.add_widget(layout)

        Window.bind(on_resize=self.on_window_resize)

    def update_pin_position(self):
        self.center_pin.pos_hint = {"center_x": 0.5, "center_y": 0.6}

    def on_window_resize(self, window, width, height):
        self.update_pin_position()

    def accept(self, instance):
        self.position = [self.map_view.lat,self.map_view.lon]

        self.manager.get_screen('add').update_position(self.position)

        self.screen_manager.current = 'add'

    def back(self, instance):
        self.screen_manager.current = 'add'

