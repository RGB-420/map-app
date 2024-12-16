from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
import math

# List of ratings (comments and scores)
valorations = [('Wow', 2), ('Increible', 8)]

class PaseoApp(MDApp):
    def build(self):
        # Creating a screen (MDScreen)
        screen = MDScreen()

        # Main layout (vertical) with spacing and padding
        main_layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        # Looping through each rating in the list of valorations
        for valoration in valorations:
            # Container for each comment and its rating
            comment_container = MDBoxLayout(orientation="horizontal")
            comment = valoration[0]  # Comment text
            rate = valoration[1]  # Rating score

            # Creating a label for the comment
            comment_label = MDLabel(text=comment)
            comment_container.add_widget(comment_label)

            # Container for the stars
            stars_container = MDBoxLayout(orientation="horizontal")
            
            # Calculate the number of full, half, and empty stars
            full_stars = int(rate / 2)
            half_star = 1 if rate % 2 != 0 else 0
            empty_stars = 5 - full_stars - half_star

            # Adding full stars
            for _ in range(full_stars):
                stars_container.add_widget(MDIcon(icon="star", icon_color=(1,1,0,0.9)))

            # Adding half star if applicable
            if half_star:
                stars_container.add_widget(MDIcon(icon="star-half", icon_color=(1,1,0,0.9)))

            # Adding empty stars
            for _ in range(empty_stars):
                stars_container.add_widget(MDIcon(icon="star-outline", icon_color=(1,1,0,0.9)))

            # Adding the stars container to the comment container
            comment_container.add_widget(stars_container)
            
            # Adding the comment container to the main layout
            main_layout.add_widget(comment_container)

        # Adding the main layout to the screen
        screen.add_widget(main_layout)
        
        return screen  # Returning the screen as the main layout

# Running the app
PaseoApp().run()
