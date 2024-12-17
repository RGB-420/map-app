import sqlite3

class Streets_db:
    #Conect to database
    def connect_db(name_db):
        return sqlite3.connect(name_db) 

    # Create the necessary tables for streets, nodes, ratings, POIs, and their respective ratings
    def create_streets_tables(con):
        cursor = con.cursor()

        # Create streets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS streets(
                 id_street INTEGER PRIMARY KEY AUTOINCREMENT,
                 street_name TEXT NOT NULL,
                 street_rating INTEGER,
                 photo BLOB,
                 width INTEGER,
                 car_lanes INTEGER,
                 street_type TEXT,
                 ground_material TEXT,
                 ground_rating INTEGER
                )
            ''')

        # Create nodes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes(
                 id_node INTEGER PRIMARY KEY AUTOINCREMENT,
                 id_street INTEGER,
                 geometry TEXT,
                 FOREIGN KEY (id_street) REFERENCES streets(id_street)
                )
            ''')
        
        # Create rating streets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rating_street (
                id_rating_street INTEGER PRIMARY KEY AUTOINCREMENT,
                id_street INTEGER,
                rating INTEGER,
                comment TEXT,
                FOREIGN KEY (id_street) REFERENCES streets(id_street)
                )
            ''')
        
        # Create rating ground streets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rating_ground_street (
                id_rating_ground_street INTEGER PRIMARY KEY AUTOINCREMENT,
                id_street INTEGER,
                rating INTEGER,
                comment TEXT,
                FOREIGN KEY (id_street) REFERENCES street(id_street)
                )
            ''')
        
        # Create POI table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS POI (
                id_POI INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT not null,
                latitude REAL not null,
                longitude REAL not null,
                photo BLOB,
                info1 TEXT,
                info2 TEXT,
                info3 TEXT,
                rating INTEGER
                )
            ''')
        
        # Create rating POI table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rating_POI (
                id_rating_POI INTEGER PRIMARY KEY AUTOINCREMENT,
                id_POI INTEGER,
                rating INTEGER,
                comment TEXT,
                FOREIGN KEY (id_POI) REFERENCES POI(id_POI)
                )
            ''')
        
        con.commit()

    # Insert a street into the database and return its ID. If the street already exists, return its existing ID.
    def insert_street(con, street_name, car_lanes):
        cursor = con.cursor()
        print(street_name) # Debug print to show the street being inserted
        cursor.execute('SELECT id_street FROM streets WHERE street_name = ?',(street_name,)) # Search if the street has an id
        result = cursor.fetchone()

        if result:
            return result[0] # Return existing street ID
        else:
            cursor.execute('INSERT INTO streets(street_name, car_lanes) VALUES (?,?)', (street_name,car_lanes,))
            con.commit() # Commit the changes
            return cursor.lastrowid  # Return the newly inserted street ID

    # Insert a node associated with a street, including latitude, longitude, and elevation
    def insert_node(con, id_street, lat, lon, elevation):
        cursor = con.cursor()
        cursor.execute('INSERT INTO nodes (id_street, latitude, longitude, elevation) VALUES (?,?,?,?)',(id_street, lat, lon, elevation))
        con.commit() # Commit the changes
