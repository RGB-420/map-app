import requests
from streets_db import Streets_db

class Data:
    # Obtain street data from Overpass API
    def get_data_overpass(city):
        # Overpass API URL
        overpass_url = "http://overpass-api.de/api/interpreter"

        # Overpass query to get streets in the given city, excluding certain types
        overpass_query = f"""
            [out:json];
            area[name="{city}"]->.searchArea;
            (
             way["highway"]["highway" != "motorway"]["highway" != "trunk"]["highway" != "motorway_link"]["highway" !="cycleway"]["highway" !="service"]["footway" != "crossing"]["access" != "private"](area.searchArea);
            );
            out body;
            >;
            out skel qt;
        """
        
        # Sending the GET request to the Overpass API
        response = requests.get(overpass_url, params={'data': overpass_query})
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json() # Return the data in JSON format
        else:
            raise Exception(f"Error obtaining data from the API: {response.status_code}")

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
        # Create a nodes dictionary for ID
        nodes_dict = {}

        # Store the nodes in the dict
        for element in data['elements']:
            if element['type'] == 'node':
                nodes_dict[element['id']] = (element['lat'], element['lon'])

        # Store the streets
        for element in data['elements']:
            if element['type'] == 'way' and 'tags' in element and 'name' in element['tags']:
                street_name = element['tags']['name']

                if element['tags'].get('lanes', None):
                    car_lanes = element['tags']['lanes']
                else:
                    car_lanes = None
                # Insert the street in the db and take the ID
                id_street = Streets_db.insert_street(con, street_name, car_lanes)

                # Insert the street nodes
                for node_id in element['nodes']:
                    if node_id in nodes_dict:
                        latitude, longitude = nodes_dict[node_id]

                        elevation = Data.get_elevation(latitude, longitude)

                        Streets_db.insert_node(con, id_street, latitude, longitude, elevation)
