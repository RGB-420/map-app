from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer

from screen.main_screen import MainScreen
from screen.menu import MenuNoUserDrawer, MenuUserDrawer
from screen.register_screen import RegisterScreen
from screen.login_screen import LoginScreen
from screen.add_screen import AddPOIScreen
from screen.ubicate_map_screen import UbiMapScreen
from screen.unused_rate_street_screen import RateStreetScreen
from screen.cam_screen import CamScreen

import os
import json

SESSION_FILE = 'session.json'

class PaseoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"

        # Create the navigation layout for the app
        self.nav_layout = MDNavigationLayout()

        # Initialize the ScreenManager
        self.sm = MDScreenManager()
        self.sm.shared_data = None

        # Add the different screens to the screen manager
        self.main_screen = MainScreen(name='main', screen_manager=self.sm)
        self.sm.add_widget(self.main_screen)

        rate_screen = RateStreetScreen(name='rate', screen_manager=self.sm)
        self.sm.add_widget(rate_screen)

        add_poi_screen = AddPOIScreen(name='add', screen_manager=self.sm)
        self.sm.add_widget(add_poi_screen)

        register_screen = RegisterScreen(name='register', screen_manager=self.sm)
        self.sm.add_widget(register_screen)

        login_screen = LoginScreen(name='login', screen_manager=self.sm)
        self.sm.add_widget(login_screen)

        ubi_map_screen = UbiMapScreen(name='ubi_map', screen_manager=self.sm)
        self.sm.add_widget(ubi_map_screen) 

        cam_screen = CamScreen(name='cam', screen_manager=self.sm)
        self.sm.add_widget(cam_screen) 
        
        #self.load_session()

        #self.main_screen.set_nav_drawer(self.nav_drawer)

        self.nav_layout.add_widget(self.sm)
        #self.nav_layout.add_widget(self.nav_drawer)

        return self.nav_layout

PaseoApp().run() 
