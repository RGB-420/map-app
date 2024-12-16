from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogContentContainer
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemTrailingCheckbox
from kivymd.uix.button import MDButtonText, MDButton
from kivy.lang import Builder
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView

class AddPOIDialog(MDDialog):
    def __init__(self, screen_manager,**kwargs):
        super().__init__(
        size_hint_x=0.9,
        size_hint_y=None,
        )
        
        self.screen_manager = screen_manager
        self.options = {
            "water": "Wasserquelle",
            "bench": "Bank",
            "container": "Container",
            "wc": "Badezimmer",
            "building": "Schönes Gebäude",
            "history": "Historischer Ort",
            "star": "Skulptur"
        }

        title=MDDialogHeadlineText(text = "Sehenwürdigkeit hinzufügen")
        self.add_widget(title)

        self.create_buttons()

        self.create_content()
            
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

    def create_buttons(self):
        container = MDDialogButtonContainer(padding = 20, spacing = 30)
        cancel_button = MDButton(MDButtonText(text="CANCEL"), style="text", on_release = self.dismiss)
        confirm_button = MDButton(MDButtonText(text="OK"), style="text", on_release = self.confirm)

        container.add_widget(cancel_button)
        container.add_widget(confirm_button)

        self.add_widget(container)
            
    def confirm(self,*args):
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
            self.screen_manager.shared_data = selected_items
            self.dismiss()
            self.screen_manager.current = 'add'

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