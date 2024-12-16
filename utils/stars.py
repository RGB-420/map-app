from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
import math

# List of ratings from 0 to 10
rate = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

class PaseoApp(MDApp):  # Defining the main class for the application
    def build(self):
        # Creating a screen (MDScreen)
        screen = MDScreen()

        # Main layout (vertical) with spacing and padding
        main_layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        # Loop through each rating in the rate list
        for rating in rate:
            # Container for each row of stars
            container = MDBoxLayout(orientation="horizontal", spacing=5)

            # Calculate the number of full, half, and empty stars
            full_stars = int(rating / 2)
            half_star = 1 if rating % 2 != 0 else 0
            empty_stars = 5 - full_stars - half_star

            # Adding full stars to the container
            for _ in range(full_stars):
                container.add_widget(MDIcon(icon="star"))

            # Adding half star if applicable
            if half_star:
                container.add_widget(MDIcon(icon="star-half"))

            # Adding empty stars to the container
            for _ in range(empty_stars):
                container.add_widget(MDIcon(icon="star-outline"))

            # Adding the container to the main layout
            main_layout.add_widget(container)

        # Adding the main layout to the screen
        screen.add_widget(main_layout)

        return screen  # Returning the screen as the main layout

# Running the app
PaseoApp().run()