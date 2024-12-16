from kivymd.uix.screen import MDScreen
from kivy.uix.camera import Camera
from kivymd.uix.button import MDIconButton, MDFabButton, MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogContentContainer, MDDialogHeadlineText
from kivy.uix.image import AsyncImage
from kivy_garden.xcamera import XCamera

import time
import os
import numpy as np
from PIL import Image as PILImage

class CamScreen(MDScreen):
    def __init__(self, screen_manager,**kwargs):
        super(CamScreen,self).__init__(**kwargs)
        self.image = None
        self.camera = None
        self.dialog = None
        
        self.screen_manager = screen_manager

    def on_enter(self):
        Clock.schedule_once(self.initialize_camera, 0)

    def initialize_camera(self, dt):
        container = MDBoxLayout(orientation="vertical")

        return_button = MDIconButton(icon="arrow-left", on_release=self.back)
        container.add_widget(return_button)

        self.camera = Camera(index=0, resolution=(320, 240), play=True)
        self.button = MDFabButton(icon="camera", pos_hint={"center_x": 0.5, "center_y": 0.2}, on_release=self.capture)

        container.add_widget(self.camera)
        container.add_widget(self.button)

        self.add_widget(container)

    def capture(self, instance):
        texture = self.camera.texture
        size = texture.size

        pixels = np.frombuffer(texture.pixels, dtype=np.uint8)
        pixels = pixels.reshape(size[1], size[0], 4)

        pil_image = PILImage.fromarray(pixels)
        pil_image = pil_image.crop((0, 0, size[0], int(size[0] * 0.75))) 

        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.image_path = f"images/POI_images/IMG_{timestr}.png"
        pil_image.save(self.image_path)

        self.confirmation_dialog()

    def confirmation_dialog(self):
        if self.dialog:
            self.dialog.dismiss()
        
        preview_image = AsyncImage(source=self.image_path, size_hint=(1, None), height=300, allow_stretch=True)

        self.dialog = MDDialog()

        title = MDDialogHeadlineText(text="Bestätigen")
        self.dialog.add_widget(title)

        container = MDDialogContentContainer()
        container.add_widget(preview_image)
        self.dialog.add_widget(container)

        buttons = MDDialogButtonContainer()
        cancel_button = MDIconButton(icon="close", on_release=self.cancel_save)
        confirm_button = MDIconButton(icon="check", on_release=self.confirm_save)

        buttons.add_widget(cancel_button)
        buttons.add_widget(confirm_button)
        self.dialog.add_widget(buttons)

        self.dialog.open()

    def confirm_save(self, *args):
        self.screen_manager.get_screen('add').update_image(self.image_path)

        self.screen_manager.current = 'add'

        self.dialog.dismiss()
        self.dialog = None

    def cancel_save(self, *args):
        if self.image_path and os.path.exists(self.image_path):
            os.remove(self.image_path)

        self.dialog.dismiss()
        self.dialog = None

    def back(self, instance):
        self.screen_manager.current = 'add'
