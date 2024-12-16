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

from io import BytesIO
import sqlite3

from screen.rating_dialog import RatingDialog

class InfoPOISheet(MDBottomSheet):
    def __init__(self, id_POI, POI_type, info1, info2, info3, photo, rating, db, *args, **kwargs):
        super(InfoPOISheet,self).__init__(*args, **kwargs)
        self.type = "modal"
        self.adaptive_height = True

        self.id_POI = id_POI
        self.POI_type = POI_type
        self.info1 = info1
        self.info2 = info2
        self.info3 = info3
        self.rating = rating
        self.db = db
        self.get_comments_db()

        self.image = None
        if photo:
            try:
                byte_data = BytesIO(photo)
                self.image = CoreImage(byte_data, ext="png").texture
                print("Imagen procesada correctamente.")
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")

        self.set_drag_handle()

        scroll_view = ScrollView(size_hint_y = None, height=Window.height*0.7)
        self.container = MDBoxLayout(orientation = "vertical", adaptive_height = True)
        self.set_image()

        self.set_tab()
        
        scroll_view.add_widget(self.container)
        self.add_widget(scroll_view)

    def set_drag_handle(self):
        drag_handle = MDBottomSheetDragHandle()

        self.title = MDBottomSheetDragHandleTitle(text=self.POI_type, font_style='Display',role="small", adaptive_height=True)
        close_button = MDBottomSheetDragHandleButton(icon = "close", on_release = self.close, ripple_effect=False)

        drag_handle.add_widget(self.title)
        drag_handle.add_widget(close_button)

        self.add_widget(drag_handle)

    def set_image(self):
        self.image_container = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15), adaptive_height=True)
        
        if self.image:

            image_width = Window.width * 0.7
            image_height = image_width * (self.image.height / self.image.width)

            image = Image(
                texture=self.image,
                size_hint=(None, None),
                width=image_width,
                height=image_height,
                allow_stretch = True,
                keep_ratio=True,
                pos_hint = {"center_x": 0.5}
            )

            self.image_container.add_widget(image)
        else:
            print("No se pudo cargar la textura para la imagen.")
        
        self.container.add_widget(self.image_container)

    def close(self, instance):
        self.set_state("close")

    def on_enter(self, *args):
        self.update_interface()

    def set_tab(self):
        tabs = MDTabsPrimary()
        self.icon1 = MDTabsItemIcon(icon="information")
        self.icon2 = MDTabsItemIcon(icon="comment")

        self.text1 = MDTabsItemText(text = "Informationen")
        self.text2 = MDTabsItemText(text = "Bewertungen")
        
        self.item1 = MDTabsItem(self.icon1, self.text1)
        self.item2 = MDTabsItem(self.icon2, self.text2)

        tabs.add_widget(self.item1)
        tabs.add_widget(self.item2)

        self.carousel = MDTabsCarousel(size_hint_y=None, height=dp(500))
        self.general_tab()
        self.review_tab()

        tabs.add_widget(self.carousel)
        self.container.add_widget(tabs)
    
    def general_tab(self):
        self.general_container = MDStackLayout(padding=dp(30), spacing=dp(20))

        self.info_boxes = [
            self.create_info_box("", "", add_separator = False),
            self.create_info_box("", "", add_separator = True),
            self.create_info_box("", "", add_separator = True),
        ]

        for box in self.info_boxes:
            self.general_container.add_widget(box)
        
        self.carousel.add_widget(self.general_container)

    def create_info_box(self, icon, text, add_separator):
        info_box = MDBoxLayout(orientation="vertical", spacing=10, adaptive_height=True)

        if add_separator:
            info_box.add_widget(MDDivider(height=dp(1)))

        horizontal_box = MDBoxLayout(orientation="horizontal", spacing=10, adaptive_height=True)
        info_icon = MDIcon(icon=icon, size_hint=(None,None), size=(dp(24),dp(24)), pos_hint={"center_y":0.5})
        info_label = MDLabel(text=text, valign="center", pos_hint={"center_y":0.5})

        horizontal_box.add_widget(info_icon)
        horizontal_box.add_widget(info_label)
        info_box.add_widget(horizontal_box)

        return info_box

    def review_tab(self):
        review_container = MDStackLayout(padding=dp(30), spacing=dp(20))
        
        general_review_container = MDBoxLayout(orientation="horizontal", padding=20, spacing=20, adaptive_height=True)

        if self.rating:
            general_review_container.add_widget(MDLabel(text=f"{self.rating/2:.1f}", font_style="Headline"))

            stars_container = self.create_stars(self.rating)

            general_review_container.add_widget(stars_container)

            review_container.add_widget(general_review_container)

        add_rating = MDButton(MDButtonText(text="Bewertung hinzufügen"),
                              MDButtonIcon(icon="plus"),
                              on_press=self.rating_click)
        
        review_container.add_widget(add_rating)

        review_container.add_widget(MDDivider(height=dp(1)))

        for valoration in self.valorations:
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
    
    def rating_click(self, instance):
        dialog = RatingDialog(self.id_POI, self.title.text, "POI")
        dialog.open()

    def update_interface(self):
        configurations = {
            "water": {
                "title": "Wasserquelle",
                "info_boxes": [
                    {"text":self.info1, "icon": "wrench"},
                    {"text":self.info2, "icon": "water-check"},
                    None
                ]
            },

            "bench": {
                "title": "Bank",
                "info_boxes": [
                    {"text": self.info1, "icon": "layers"},
                    {"text": self.info2, "icon": "seat-passenger"},
                    None
                ]
            },

            "container": {
                "title": "Container",
                "info_boxes": [
                    {"text": self.info1, "icon": "wrench"},
                    None,
                    None
                ]
            },

            "wc": {
                "title": "Badezimmer",
                "info_boxes": [
                    {"text": self.info1, "icon": "office-building"},
                    {"text": self.info2, "icon": "arrow-decision"},
                    {"text": self.info3, "icon": "clock"}
                ]
            },

            "building": {
                "title": self.info1,
                "info_boxes": [
                    {"text": self.info2, "icon": "math-compass"},
                    {"text": self.info3, "icon": "camera-marker"},
                    None
                ]
            },

            "history": {
                "title": self.info1,
                "info_boxes": [
                    {"text": self.info2, "icon": "book-open-page-variant"},
                    None,
                    None
                ]
            },

            "star": {
                "title": self.info1,
                "info_boxes": [
                    {"text": self.info2, "icon": "account"},
                    None,
                    None
                ]
            }
        }
        
        config = configurations.get(self.POI_type)
        if not config:
            return
        
        self.title.text = config["title"]

        for idx, info in enumerate(config["info_boxes"]):
            box = self.info_boxes[idx]
            if info is None:
                if box in self.general_container.children:
                    self.general_container.remove_widget(box)
            
            else:
                if box not in self.general_container.children:
                    self.general_container.add_widget(box)
                icon = box.children[0].children[1]
                label = box.children[0].children[0]
                icon.icon = info["icon"]
                label.text = info["text"]

    def get_comments_db(self):
        con = sqlite3.connect(self.db)
        cursor = con.cursor()

        cursor.execute('SELECT comment, rating FROM rating_POI WHERE id_POI = ?', (self.id_POI,))
        self.valorations = cursor.fetchall()

        con.commit()
        con.close()

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