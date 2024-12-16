from kivymd.uix.screen import MDScreen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.appbar import MDTopAppBar
from kivy_garden.mapview import  MapMarkerPopup, MapMarker
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu, MDNavigationDrawerLabel
from kivymd.uix.button import MDFabButton
from kivy.core.window import Window
from kivy.clock import Clock

import sqlite3
from functools import partial
from plyer import gps

from screen.map import Map
from screen.street_creator import StreetCreator
from screen.add_POI_dialog import AddPOIDialog
from screen.info_POI_sheet import InfoPOISheet
from screen.info_street_sheet import InfoStreetSheet

class MainScreen(MDScreen):
    def __init__(self, screen_manager,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.nav_drawer = None
        self.screen_manager = screen_manager
        self.map_interaction_enabled = True

        layout = BoxLayout(orientation='vertical')

        self.create_topBar()
        layout.add_widget(self.toolbar)

        content = FloatLayout(size_hint=(1,1))
    
        # Add the map
        self.map_view = Map.build_map(41.3674,2.0567)
        content.add_widget(self.map_view)
        
        # Detect map touch
        self.map_view.bind(on_touch_up=self.on_map_touch)

        self.db = 'db.sql'

        self.street_creator = StreetCreator(map_view=self.map_view, db = self.db, nodes = [], id_street = 0)
        content.add_widget(self.street_creator)

        self.add_button = MDFabButton(icon="plus",on_release=self.on_add_click, on_press=self.disable_map_interaction, pos_hint= {"x": 0.8, "y": 0.1})
        content.add_widget(self.add_button)
        self.dialog = AddPOIDialog(screen_manager=self.screen_manager)
        
        #self.a_button = MDFabButton(icon="close",on_release=self.get_location, on_press=self.disable_map_interaction, pos_hint= {"x": 0.8, "y": 0.5})
        #content.add_widget(self.a_button)

        self.info_poi_sheet = None
        self.info_street_sheet = None

        Clock.schedule_interval(self.update_bottom_sheet_status, 0.1)

        self.draw_streets()

        self.update_POI() 

        layout.add_widget(content)
        
        self.add_widget(layout)
    
    def set_nav_drawer(self, nav_drawer):
        self.nav_drawer = nav_drawer

    def on_map_touch(self, instance, touch):
        if not self.map_interaction_enabled:
            return
        if not self.map_view.collide_point(*touch.pos):
            return
        if touch.is_mouse_scrolling:
            return
        if self.map_move(touch):
            return
        if self.dialog._is_open:
            return
        
        id_rated_street = self.street_creator.near_street(touch.x, touch.y)
        if id_rated_street:
            self.show_info_street_sheet(id_rated_street)
    
    def show_info_street_sheet(self,id_street):    
        if self.info_street_sheet:
            return
        else:
            self.info_street_sheet = InfoStreetSheet(id_street, self.db)

            self.add_widget(self.info_street_sheet)

            self.info_street_sheet.set_state("open")

    def draw_streets(self): 
        self.add_widget(self.street_creator)
    
    def get_street_nodes(self, id_street):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
    
        cursor.execute('''SELECT latitude, longitude 
                      FROM nodes
                        WHERE id_street = ?''',
                        (id_street,))
     
        nodes = cursor.fetchall()
    
        conn.close()
        return nodes

    def get_all_street_ids(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT id_street FROM nodes')
        id_streets = cursor.fetchall()
        conn.close()

        return [id_street[0] for id_street in id_streets]

    def draw_streets(self, *args):
        id_streets = self.get_all_street_ids()
        for id_street in id_streets:
            nodes = self.get_street_nodes(id_street)
            self.street_creator.add_street(nodes, id_street)

    def map_move(self, touch):
        move = False
        if touch.opos == touch.pos:
            return move
        else:
            move = True
            return move

    def create_topBar(self):
        self.toolbar = MDTopAppBar(type="small", size_hint_x = 1, pos_hint={"center_x": .5, "center_y": .5})
        self.toolbar.left_action_items = [["menu", lambda x: self.nav_drawer.set_state("open")]]

    def update_POI(self):
        source = None
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute('SELECT id_POI, type, latitude, longitude, info1, info2, info3, photo, rating FROM POI')
        pois = cursor.fetchall()

        conn.close()

        for id_POI, type, lat, lon, info1, info2, info3, photo, rating in pois:
            source = f"images/POI_icons/marker_{type}.png"

            marker = MapMarkerPopup(source=source, lat=lat, lon=lon, on_press=self.disable_map_interaction)

            marker.bind(on_release=partial(self.show_info_poi_sheet, id_POI, type, info1, info2, info3, photo, rating))
            marker.size = [70, 70]

            self.map_view.add_marker(marker)

    def on_add_click(self, instance):
        self.dialog.open()
        self.map_interaction_enabled = True

    def disable_map_interaction(self, instance):
        self.map_interaction_enabled = False

    def show_info_poi_sheet(self, id_POI, type, info1, info2, info3, photo, rating, marker):
        if self.info_poi_sheet:
            return
        else:
            self.info_poi_sheet = InfoPOISheet(id_POI, type, info1, info2, info3, photo, rating)

            self.add_widget(self.info_poi_sheet)

            self.info_poi_sheet.set_state("open")

    def update_bottom_sheet_status(self, dt):
        if self.info_poi_sheet and self.info_poi_sheet.status=="closed":
            self.info_poi_sheet = None
            self.map_interaction_enabled = True

        if self.info_street_sheet and self.info_street_sheet.status=="closed":
            self.info_street_sheet = None
    
    def get_location(self, instance):
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=1)  # Request location updates every second or on significant movement
        except NotImplementedError:

            print("GPS no implementado en esta plataforma")

    def on_location(self, *kwargs):
        latitude = kwargs.get("lat")
        longitude = kwargs.get("lon")

        if latitude and longitude:
            self.map_view.center_on(latitude, longitude)

            marker = MapMarker(source="images/marker.png", lat=latitude, lon=longitude)
            self.map_view.add_marker(marker)