import requests
import osmnx as ox

from streets_db import Streets_db

class Data:
    # Obtain street data from Overpass API
    def get_data(city):
        graph = ox.graph_from_place(city, network_type="walk")
        _, Data.edges = ox.graph_to_gdfs(graph)
                

    # Function to get the elevation for a given latitude and longitude using the Open-Elevation API
    def get_elevation(latitude, longitude):
        url = "http://localhost:5000/v1/eudem25m"  # Open-Elevation API endpoint
        params = {"locations": f"{latitude},{longitude}"} # Parameters containing the coordinates
        try:
            # Send the GET request to the Open-Elevation API
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for any HTTP errors
            data = response.json()  # Parse the JSON response

            # Check if the response contains elevation data
            if "results" in data and len(data["results"]) > 0:
                return data["results"][0]["elevation"]
            else:
                print(f"No elevation found for ({latitude}, {longitude})")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Open-Elevation: {e}")
            return None

    # Process data from API and store it in the db
    def process_data(con, data):
        for _, edge in Data.edges.iterrows():
            if edge["geometry"] is not None:
                name = edge.get("name", "Calle Sosa")

                if isinstance(name, list):
                    name = name[0]

                geometry = edge["geometry"].wkt

                id_street = Streets_db.insert_street(con, name)

                Streets_db.insert_node(con, id_street, geometry)
