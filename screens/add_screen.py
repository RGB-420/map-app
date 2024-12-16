from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButtonText, MDIconButton, MDButton
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.label import MDLabel

import sqlite3

class AddPOIScreen(MDScreen):
    def __init__(self,screen_manager,**kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.db = 'db.sql'

        self.selected_item = self.screen_manager.shared_data

        self.container = None     

        self.position = [0,0]

        self.image = None

    def setup_interface(self):
        self.container = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20
            )
        return_button = MDIconButton(icon="arrow-left", on_release=self.back)
        self.container.add_widget(return_button)
        
        self.title = MDLabel(text=" ", font_style = "Headline", halign = "center")
        self.container.add_widget(self.title)

        self.info1_input = MDTextField(mode="outlined")
        self.info1_text = MDTextFieldHintText(text="")
        self.info1_input.add_widget(self.info1_text)
        self.container.add_widget(self.info1_input)

        self.info2_input = MDTextField(mode="outlined")
        self.info2_text = MDTextFieldHintText(text="")
        self.info2_input.add_widget(self.info2_text)
        self.container.add_widget(self.info2_input)

        self.info3_input = MDTextField(mode="outlined")
        self.info3_text = MDTextFieldHintText(text="")
        self.info3_input.add_widget(self.info3_text)
        self.container.add_widget(self.info3_input)
        
        box_layout = BoxLayout(orientation='horizontal')

        ubicate_button = MDIconButton(icon="map-search",halign="right", on_press=self.ubicate_click)
        box_layout.add_widget(ubicate_button)

        cam_button = MDIconButton(icon="camera",halign="center", on_press=self.cam_click)
        box_layout.add_widget(cam_button)

        self.error = MDLabel()
        box_layout.add_widget(self.error)

        continue_button = MDButton(MDButtonText(text="Continue"), on_press=self.continue_click)
        box_layout.add_widget(continue_button)

        self.container.add_widget(box_layout)

        self.add_widget(self.container)

    def ubicate_click(self, instance):
        self.screen_manager.current = 'ubi_map'

    def cam_click(self, instance):
        self.screen_manager.current = 'cam'

    def continue_click(self, instance):
        if self.position == [0,0]:
            self.error.text = "Fehlende Position" 
        
        else:
            self.update_db()
        
            self.manager.get_screen('main').update_POI()

            self.screen_manager.current = 'main'

    def update_db(self):
        image_data = None
        if self.image:
            with open(self.image, 'rb') as file:
                image_data = file.read()

        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO POI (type, latitude, longitude, photo, info1, info2, info3) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.selected_item, self.position[0], self.position[1], image_data, self.info1_input.text, self.info2_input.text, self.info3_input.text,))

        conn.commit()
        conn.close()

    def update_position(self, position):
        self.position = position

    def update_image(self, image):
        self.image = image

    def back(self, instance):
        self.screen_manager.current = 'main'

    def on_pre_enter(self,*args):
        if self.screen_manager.shared_data:
            self.selected_item = self.screen_manager.shared_data[0]
            self.screen_manager.shared_data = None

            if self.container:
                self.remove_widget(self.container)

            self.setup_interface()
            self.update_interface()

    def update_interface(self):
        configurations = {
            "water": {
                "title": "Wasserquelle",
                "info1": "Modell",
                "info2": "Wasserqualität",
                "remove_widgets": [self.info3_input]
            },

            "bench": {
                "title": "Bank",
                "info1": "Material",
                "info2": "Komfort",
                "remove_widgets": [self.info3_input]
            },

            "container": {
                "title": "Container",
                "info1": "Modell",
                "remove_widgets": [self.info2_input, self.info3_input]
            },

            "wc": {
                "title": "Badezimmer",
                "info1": "Gebäude",
                "info2": "Wegbeschreibung",
                "info3": "Zeitplan",
                "remove_widgets": []
            },

            "building": {
                "title": "Schönes Gebäude",
                "info1": "Name",
                "info2": "Architektur",
                "info3": "Beste Aussichten",
                "remove_widgets": []
            },

            "history": {
                "title": "Historischer Ort",
                "info1": "Titel",
                "info2": "Anekdote",
                "remove_widgets": [self.info3_input]
            },

            "star": {
                "title": "Skulptur",
                "info1": "Name",
                "info2": "Bildhauer",
                "remove_widgets": [self.info3_input]
            }
        }
        
        config = configurations.get(self.selected_item)
        if not config:
            return
        
        self.title.text = config.get("title", "")
        self.info1_text.text = config.get("info1", "")
        self.info2_text.text = config.get("info2", "")
        self.info3_text.text = config.get("info3", "")

        for widget in config.get("remove_widgets", []):
            if widget in self.container.children:
                self.container.remove_widget(widget)