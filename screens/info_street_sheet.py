from kivymd.uix.bottomsheet import MDBottomSheet, MDBottomSheetDragHandle, MDBottomSheetDragHandleButton, MDBottomSheetDragHandleTitle
from kivymd.uix.tab import MDTabsItem, MDTabsItemIcon, MDTabsCarousel, MDTabsPrimary, MDTabsItemText
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.image import Image as CoreImage
from kivymd.uix.divider import MDDivider
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.stacklayout import MDStackLayout
from kivy.metrics import dp
from kivy.core.window import Window

import sqlite3
from io import BytesIO
from functools import partial

from screen.rating_dialog import RatingDialog
from screen.add_info_dialog import AddWidthDialog, AddCarsDialog, AddTypeDialog, AddGroundDialog

class InfoStreetSheet(MDBottomSheet):
    def __init__(self, id_street, db, *args, **kwargs):
        super(InfoStreetSheet,self).__init__(*args, **kwargs)
        self.type = "modal"
        self.adaptive_height = True

        self.db = db
        self.id_street = id_street

        self.get_db_data()

        self.set_drag_handle()

        scroll_view = ScrollView(size_hint_y = None, height=Window.height*0.7)
        self.container = MDBoxLayout(orientation = "vertical", adaptive_height = True)

        self.set_image()

        self.set_tab()

        scroll_view.add_widget(self.container)
        self.add_widget(scroll_view)

    def set_drag_handle(self):
        drag_handle = MDBottomSheetDragHandle()

        self.title = MDBottomSheetDragHandleTitle(text=self.street_name, font_style='Display',role="small", adaptive_height=True)
        close_button = MDBottomSheetDragHandleButton(icon = "close", on_release = self.close, ripple_effect=False)

        drag_handle.add_widget(self.title)
        drag_handle.add_widget(close_button)

        self.add_widget(drag_handle)

    def set_image(self):
        if self.photo:
            try:
                byte_data = BytesIO(self.photo)
                self.image = CoreImage(byte_data, ext="png").texture
                print("Imagen procesada correctamente.")
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
        
        self.image_container = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15), adaptive_height=True)
        
        if self.photo:
            image_width = Window.width * 0.7
            image_height = image_width * (self.image.height / self.image.width)

            image = Image(
                texture=self.photo,
                size_hint=(None, None),
                width=image_width,
                height=image_height,
                allow_stretch = True,
                keep_ratio=True,
                pos_hint = {"center_x": 0.5}
            )

            self.image_container.add_widget(image)
        else:
            button_camera = MDButton(MDButtonIcon(icon="camera-plus"))
            self.image_container.add_widget(button_camera)

        self.container.add_widget(self.image_container)

    def set_tab(self):
        tabs = MDTabsPrimary()
        self.icon1 = MDTabsItemIcon(icon = "information")
        self.icon2 = MDTabsItemIcon(icon = "comment")
        self.icon3 = MDTabsItemIcon(icon = "layers")

        self.text1 = MDTabsItemText(text = "Informationen")
        self.text2 = MDTabsItemText(text = "Bewertungen")
        self.text3 = MDTabsItemText(text = "Boden")
        
        self.item1 = MDTabsItem(self.icon1, self.text1)
        self.item2 = MDTabsItem(self.icon2, self.text2)
        self.item3 = MDTabsItem(self.icon3, self.text3)

        tabs.add_widget(self.item1)
        tabs.add_widget(self.item2)
        tabs.add_widget(self.item3)

        self.carousel = MDTabsCarousel(size_hint_y=None, height=dp(500))
        self.general_tab()
        self.review_tab()
        self.ground_tab()

        tabs.add_widget(self.carousel)
        self.container.add_widget(tabs)

    def general_tab(self):
        self.general_container = MDStackLayout(padding=dp(30), spacing=dp(20))

        self.info_boxes = [
            self.create_info_box("arrow-split-vertical", str(self.width_street), add_separator = False, button_id="width"),
            self.create_info_box("car", str(self.car_lanes), add_separator = True, button_id="car"),
            self.create_info_box("content-paste", self.street_type, add_separator = True, button_id="street_type"),
        ]

        for box in self.info_boxes:
            self.general_container.add_widget(box)
        
        self.carousel.add_widget(self.general_container)
    
    def create_info_box(self, icon, text, add_separator, button_id):
        info_box = MDBoxLayout(orientation="vertical", spacing=10, adaptive_height=True)

        if add_separator:
            info_box.add_widget(MDDivider(height=dp(1)))

        horizontal_box = MDBoxLayout(orientation="horizontal", spacing=10, adaptive_height=True)
        
        info_icon = MDIcon(icon=icon, size_hint=(None,None), size=(dp(24),dp(24)), pos_hint={"center_y":0.5})
        horizontal_box.add_widget(info_icon)   

        if text and text != "None":         
            info_label = MDLabel(text=text, valign="center", pos_hint={"center_y":0.5})

            horizontal_box.add_widget(info_label)
        else:
            add_button = MDButton(MDButtonIcon(icon="plus"), on_press=self.show_add_info_dialog)

            add_button.id = button_id

            horizontal_box.add_widget(add_button)

        info_box.add_widget(horizontal_box)

        return info_box

    def review_tab(self):
        review_container = MDStackLayout(padding=dp(30), spacing=dp(20))
        
        general_review_container = MDBoxLayout(orientation="horizontal", padding=20, spacing=20, adaptive_height=True)

        if self.street_rating:
            general_review_container.add_widget(MDLabel(text=f"{self.street_rating/2:.1f}", font_style="Headline"))

            stars_container = self.create_stars(self.street_rating)

            general_review_container.add_widget(stars_container)

            review_container.add_widget(general_review_container)

        add_rating = MDButton(MDButtonText(text="Bewertung hinzufügen"),
                              MDButtonIcon(icon="plus"),
                              on_press=self.rating_street_click)
        
        review_container.add_widget(add_rating)

        review_container.add_widget(MDDivider(height=dp(1)))

        for valoration in self.general_valorations:
            comment_container = MDBoxLayout(orientation="horizontal", padding=20, spacing=20, size_hint=(1, None), adaptive_height=True)
            comment = valoration[0]
            rate = valoration[1]

            comment_label = MDLabel(text=comment)
            comment_container.add_widget(comment_label)

            stars_container = self.create_stars(rate)
            comment_container.add_widget(stars_container)

            review_container.add_widget(comment_container)

            review_container.add_widget(MDDivider(height=dp(1)))
        
        self.carousel.add_widget(review_container)
    
    def rating_street_click(self, instance):
        dialog = RatingDialog(self.id_street, self.title.text, "street")
        dialog.open()

    def ground_tab(self):
        ground_container = MDStackLayout(padding=dp(30), spacing=dp(20))

        ground_container.add_widget(self.create_info_box("hammer-screwdriver", self.ground_material, add_separator=False, button_id="ground"))
        ground_container.add_widget(MDDivider(height=dp(1)))

        ground_review_container = MDBoxLayout(orientation="horizontal", padding=20, spacing=20, adaptive_height=True)

        if self.ground_rating:
            ground_review_container.add_widget(MDLabel(text=f"{self.ground_rating/2:.1f}", font_style="Headline"))

            stars_container = self.create_stars(self.ground_rating)

            ground_review_container.add_widget(stars_container)

            ground_container.add_widget(ground_review_container)

        add_rating = MDButton(MDButtonText(text="Bewertung hinzufügen"),
                              MDButtonIcon(icon="plus"),
                              on_press=self.rating_ground_click)
        
        ground_container.add_widget(add_rating)

        ground_container.add_widget(MDDivider(height=dp(1)))

        for valoration in self.ground_valorations:
            comment_container = MDBoxLayout(orientation="horizontal", padding=20, spacing=20, size_hint=(1, None), adaptive_height=True)
            comment = valoration[0]
            rate = valoration[1]

            comment_label = MDLabel(text=comment)
            comment_container.add_widget(comment_label)

            stars_container = self.create_stars(rate)
            comment_container.add_widget(stars_container)

            ground_container.add_widget(comment_container)

            ground_container.add_widget(MDDivider(height=dp(1)))
        
        self.carousel.add_widget(ground_container)

    def rating_ground_click(self, instance):
        dialog = RatingDialog(self.id_street, self.title.text, "ground")
        dialog.open()

    def get_db_data(self):
        con = sqlite3.connect(self.db)
        cursor = con.cursor()

        cursor.execute('SELECT latitude,longitude,elevation FROM nodes WHERE id_street = ?', (self.id_street,))
        self.nodes = cursor.fetchall()

        cursor.execute('SELECT street_name, street_rating, photo, width, car_lanes, street_type, ground_material, ground_rating FROM streets WHERE id_street = ?', (self.id_street,))
        street = cursor.fetchone()

        cursor.execute('SELECT comment, rating FROM rating_street WHERE id_street = ?', (self.id_street,))
        self.general_valorations = cursor.fetchall()

        cursor.execute('SELECT comment, rating FROM rating_ground_street WHERE id_street = ?', (self.id_street,))
        self.ground_valorations = cursor.fetchall()

        self.street_name = street[0]
        self.street_rating = street[1]
        self.photo = street[2]
        self.width_street = street[3]
        self.car_lanes = street[4]
        self.street_type = street[5]
        self.ground_material = street[6]
        self.ground_rating = street[7]

        con.commit()
        con.close()

    def show_add_info_dialog(self, instance):
        button_id = getattr(instance, "id", None)
        if button_id == "width":
            dialog = AddWidthDialog(self.id_street, self.db)

        if button_id == "car":
            dialog = AddCarsDialog(self.id_street, self.db)
        
        if button_id == "street_type":
            dialog = AddTypeDialog(self.id_street, self.db)

        if button_id == "ground":
            dialog = AddGroundDialog(self.id_street, self.db)

        dialog.open()
        
    def close(self, instance):
        self.set_state("close")

    def create_stars(self, rating):
        stars_container = MDBoxLayout(orientation="horizontal", pos_hint={"center_x": 0.5})
        full_stars = int(rating / 2)
        half_star = 1 if rating % 2 != 0 else 0
        empty_stars = 5 - full_stars - half_star

        for _ in range(full_stars):
            stars_container.add_widget(MDIcon(icon="star", icon_color=(1,1,0,0.9)))

        if half_star:
            stars_container.add_widget(MDIcon(icon="star-half", icon_color=(1,1,0,0.9)))

        for _ in range(empty_stars):
            stars_container.add_widget(MDIcon(icon="star-outline", icon_color=(1,1,0,0.9)))

        return stars_container