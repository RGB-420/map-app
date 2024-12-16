from streets_db import Streets_db
from data import Data

class StreetsDataBase:
    # List of cities for which we will gather street data
    cities = ["Sant Joan Despí", "Esplugues de Llobregat", "l'Hospitalet de Llobregat", "Sant Just Desvern", "Cornellà de Llobregat"]

    # Connect to the database (using SQLite in this case)
    con = Streets_db.connect_db("db.sql")

    # Create the necessary tables for storing street data in the database
    Streets_db.create_streets_tables(con)

    # Loop through each city and retrieve the street data
    for city in cities:
        # Get street data for the current city from Overpass API
        data = Data.get_data_overpass(city)

        # Process the retrieved data and insert it into the database
        Data.process_data(con, data)

    # Close the database connection after all data has been processed
    con.close()