from kivy_garden.mapview import MapView, MapSource

class Map:
    def __init__(self):
        pass
    
    @staticmethod
    def build_map(lat,long):
        mapa = MapView(zoom=15, lat = lat, lon = long)
        return mapa
        