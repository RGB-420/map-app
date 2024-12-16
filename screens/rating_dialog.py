from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogContentContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.slider import MDSlider, MDSliderHandle
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldLeadingIcon
from kivymd.uix.label import MDLabel

import sqlite3

class RatingDialog(MDDialog):
    def __init__(self, id, title, type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number = id
        self.title = title
        self.type = type

        self.mean_valoration = None

        self.create_buttons()
        self.create_content()

    def create_buttons(self):
        container = MDDialogButtonContainer(padding = 20, spacing = 30)
        cancel_button = MDButton(MDButtonText(text="CANCEL"), style="text", on_release = self.dismiss)
        confirm_button = MDButton(MDButtonText(text="OK"), style="text", on_release = self.confirm)

        container.add_widget(cancel_button)
        container.add_widget(confirm_button)

        self.add_widget(container)

    def create_content(self):
        container = MDDialogContentContainer(orientation="vertical")

        title_label = MDLabel(text=self.title, font_style="Headline")
        container.add_widget(title_label)

        self.rating_slider = MDSlider(MDSliderHandle(), step=1, value=5, max=10, size_hint_y=None)
        container.add_widget(self.rating_slider)

        self.comment_text = MDTextField()
        self.comment_text.add_widget(MDTextFieldHintText(text="Comment"))
        container.add_widget(self.comment_text)

        self.add_widget(container)

    def confirm(self, instance):
        self.rating = self.rating_slider.value
        self.comment = self.comment_text.text
        self.update_db()
        self.dismiss()

    def update_db(self):
        queries = {
        "POI": {
            "insert": "INSERT INTO rating_POI (id_POI, rating, comment) VALUES (?, ?, ?)",
            "select_avg": "SELECT AVG(rating) FROM rating_POI WHERE id_POI = ?",
            "update": "UPDATE POI SET rating = ? WHERE id_POI = ?"
        },
        "street": {
            "insert": "INSERT INTO rating_street (id_street, rating, comment) VALUES (?, ?, ?)",
            "select_avg": "SELECT AVG(rating) FROM rating_street WHERE id_street = ?",
            "update": "UPDATE streets SET street_rating = ? WHERE id_street = ?"
        },
        "ground": {
            "insert": "INSERT INTO rating_ground_street (id_street, rating, comment) VALUES (?, ?, ?)",
            "select_avg": "SELECT AVG(rating) FROM rating_ground_street WHERE id_street = ?",
            "update": "UPDATE streets SET ground_rating = ? WHERE id_street = ?"
        }
    }

        try:
            con = sqlite3.connect('db_SJD.sql')
            cursor = con.cursor()

            if self.type in queries:
                q = queries[self.type]

                cursor.execute(q["insert"], (self.number, self.rating, self.comment))

                cursor.execute(q["select_avg"], (self.number,))
                self.mean_valoration = round(cursor.fetchone()[0])

                cursor.execute(q["update"], (self.mean_valoration, self.number))

            con.commit()

        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            con.close()
    
    def get_valoration(self):
        return self.mean_valoration