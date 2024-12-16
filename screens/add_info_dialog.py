from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogContentContainer, MDDialogHeadlineText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField,MDTextFieldHintText
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemTrailingCheckbox
from kivy.metrics import dp

import sqlite3

class AddWidthDialog(MDDialog):
    def __init__(self, id_street, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_street = id_street
        self.db = db

        self.add_widget(MDDialogHeadlineText(text="Breite hinzufügen"))

        self.create_buttons()

        self.create_content()

    def create_buttons(self):
        container = MDDialogButtonContainer(padding = dp(20), spacing = dp(20))
        cancel_button = MDButton(MDButtonText(text="CANCEL"), style="text", on_release = self.dismiss)
        confirm_button = MDButton(MDButtonText(text="OK"), style="text", on_release = self.confirm)

        container.add_widget(cancel_button)
        container.add_widget(confirm_button)

        self.add_widget(container)
    
    def create_content(self):
        container = MDDialogContentContainer(orientation="vertical", padding=dp(20), spacing=dp(20))

        self.width_text = MDTextField(MDTextFieldHintText(text="Breite"))
        container.add_widget(self.width_text)

        self.error_label = MDLabel(text="", font_style="Label", text_color=(1,0,0,1))
        container.add_widget(self.error_label)

        self.add_widget(container)

    def confirm(self, instance):
        try:
            self.street_width = int(self.width_text.text)
            con = sqlite3.connect(self.db)
            cursor = con.cursor()

            cursor.execute("UPDATE streets SET width = ? WHERE id_street = ?", (self.street_width, self.id_street,))

            con.commit()
            con.close()

            self.dismiss()
            
        except Exception as e:
            self.error_label.text = "Nur Zahlen"
            self.width_text.error = True

class AddCarsDialog(MDDialog):
    def __init__(self, id_street, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_street = id_street
        self.db = db

        self.add_widget(MDDialogHeadlineText(text="Linienwagen hinzufügen"))

        self.create_buttons()

        self.create_content()

    def create_buttons(self):
        container = MDDialogButtonContainer(padding = dp(20), spacing = dp(20))
        cancel_button = MDButton(MDButtonText(text="CANCEL"), style="text", on_release = self.dismiss)
        confirm_button = MDButton(MDButtonText(text="OK"), style="text", on_release = self.confirm)

        container.add_widget(cancel_button)
        container.add_widget(confirm_button)

        self.add_widget(container)
    
    def create_content(self):
        container = MDDialogContentContainer(orientation="vertical", padding=dp(20), spacing=dp(20))

        self.cars_text = MDTextField(MDTextFieldHintText(text="Linienwagen"))
        container.add_widget(self.cars_text)

        self.error_label = MDLabel(text="", font_style="Label", text_color=(1,0,0,1))
        container.add_widget(self.error_label)

        self.add_widget(container)

    def confirm(self, instance):
        try:
            self.car_lines = int(self.cars_text.text)
            con = sqlite3.connect(self.db)
            cursor = con.cursor()

            cursor.execute("UPDATE streets SET car_lanes = ? WHERE id_street = ?", (self.car_lines, self.id_street,))

            con.commit()
            con.close()

            self.dismiss()
            
        except Exception as e:
            self.error_label.text = "Nur Zahlen"
            self.cars_text.error = True
        
class AddTypeDialog(MDDialog):
    def __init__(self, id_street, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_street = id_street
        self.db = db

        self.options = {
            "avenue": "Alle",
            "rambla": "Rambla",
            "residential": "Wohnen",
            "commercial": "Geschäftsstraße",
            "industrial": "Industrie",
            "path": "Straße"
        }

        self.add_widget(MDDialogHeadlineText(text="Typ hinzufügen"))

        self.create_buttons()

        self.create_content()

    def create_buttons(self):
        container = MDDialogButtonContainer(padding = dp(20), spacing = dp(20))
        cancel_button = MDButton(MDButtonText(text="CANCEL"), style="text", on_release = self.dismiss)
        confirm_button = MDButton(MDButtonText(text="OK"), style="text", on_release = self.confirm)

        container.add_widget(cancel_button)
        container.add_widget(confirm_button)

        self.add_widget(container)
    
    def create_content(self):
        container = MDDialogContentContainer()
        self.list_view = MDList()

        for identifier, text in self.options.items():
            item = MDListItem()

            headline = MDListItemHeadlineText(text=text)
            checkbox = MDListItemTrailingCheckbox()

            checkbox.id = identifier

            checkbox.bind(active=self.on_checkbox_active)

            item.add_widget(headline)
            item.add_widget(checkbox)
            self.list_view.add_widget(item)
        
        container.add_widget(self.list_view)

        self.add_widget(container)

    def confirm(self, instance):
        selected_items = []

        for item in self.list_view.children:
            selected_items = []

        for item in self.list_view.children:
        
            checkbox = self.find_widget_by_type(item, MDListItemTrailingCheckbox)
        
            if checkbox and checkbox.active:
                headline = self.find_widget_by_type(item, MDListItemHeadlineText)
                if headline:
                    selected_items.append(checkbox.id)

        if selected_items:
            con = sqlite3.connect(self.db)
            cursor = con.cursor()

            cursor.execute("UPDATE streets SET street_type = ? WHERE id_street = ?", (selected_items[0], self.id_street,))

            con.commit()
            con.close()

            self.dismiss()

    def find_widget_by_type(self, widget, widget_type):
        if isinstance(widget, widget_type):
            return widget
        for child in widget.children:
            result = self.find_widget_by_type(child, widget_type)
            if result:
                return result
        return None
    
    def on_checkbox_active(self, checkbox, active):
        if active:
            for item in self.list_view.children:
                other_checkbox = self.find_widget_by_type(item, MDListItemTrailingCheckbox)
                if other_checkbox and other_checkbox != checkbox:
                    other_checkbox.active = False
    
class AddGroundDialog(MDDialog):
    def __init__(self, id_street, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_street = id_street
        self.db = db

        self.options = {
            "cement": "Zement",
            "stone": "Stein",
            "cobblestone": "Kopfsteinpflaster",
            "soil": "Boden"
        }

        self.add_widget(MDDialogHeadlineText(text="Mahlgut hinzufügen"))

        self.create_buttons()

        self.create_content()

    def create_buttons(self):
        container = MDDialogButtonContainer(padding = dp(20), spacing = dp(20))
        cancel_button = MDButton(MDButtonText(text="CANCEL"), style="text", on_release = self.dismiss)
        confirm_button = MDButton(MDButtonText(text="OK"), style="text", on_release = self.confirm)

        container.add_widget(cancel_button)
        container.add_widget(confirm_button)

        self.add_widget(container)
    
    def create_content(self):
        container = MDDialogContentContainer()
        self.list_view = MDList()

        for identifier, text in self.options.items():
            item = MDListItem()

            headline = MDListItemHeadlineText(text=text)
            checkbox = MDListItemTrailingCheckbox()

            checkbox.id = identifier

            checkbox.bind(active=self.on_checkbox_active)

            item.add_widget(headline)
            item.add_widget(checkbox)
            self.list_view.add_widget(item)
        
        container.add_widget(self.list_view)

        self.add_widget(container)

    def confirm(self, instance):
        selected_items = []

        for item in self.list_view.children:
            selected_items = []

        for item in self.list_view.children:
        
            checkbox = self.find_widget_by_type(item, MDListItemTrailingCheckbox)
        
            if checkbox and checkbox.active:
                headline = self.find_widget_by_type(item, MDListItemHeadlineText)
                if headline:
                    selected_items.append(checkbox.id)

        if selected_items:
            con = sqlite3.connect(self.db)
            cursor = con.cursor()

            cursor.execute("UPDATE streets SET ground_material = ? WHERE id_street = ?", (selected_items[0], self.id_street,))

            con.commit()
            con.close()

            self.dismiss()

    def find_widget_by_type(self, widget, widget_type):
        if isinstance(widget, widget_type):
            return widget
        for child in widget.children:
            result = self.find_widget_by_type(child, widget_type)
            if result:
                return result
        return None
    
    def on_checkbox_active(self, checkbox, active):
        if active:
            for item in self.list_view.children:
                other_checkbox = self.find_widget_by_type(item, MDListItemTrailingCheckbox)
                if other_checkbox and other_checkbox != checkbox:
                    other_checkbox.active = False
