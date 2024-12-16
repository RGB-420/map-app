from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.clock import Clock

from utils.math_utils import haversine, distance_to_segment

class StreetCreator(Widget):
    def __init__(self, map_view, db, nodes, id_street, **kwargs):
        super(StreetCreator,self).__init__(**kwargs)
        self.map_view = map_view
        self.db = db
        self.nodes = nodes
        self.id_street = id_street

        self.lines = {}
        self.all_nodes = {}

        self.nearest_node_order(nodes)

        self.draw_street()

        self.trigger_update_street_lines = Clock.create_trigger(self.update_all_street_lines, 0.1)

        self.map_view.bind(pos=self.schedule_update, size=self.schedule_update, zoom=self.schedule_update, on_touch_move= self.schedule_update)
        
    def draw_street(self):       
        with self.canvas:
            Color(0,0,0,0)   
            self.lines[self.id_street] = Line(width = 5) 
            self.update_street_lines(self.nodes, self.id_street)    

    def update_street_lines(self, nodes, id_street):
        coords = []
        for lat, lon in nodes:
            x, y = self.get_window_xy(lat, lon)
            coords.extend([x, y])

        if coords:
            self.lines[id_street].points = coords   
        else:
            self.lines

    def update_all_street_lines(self, *args):
        for id_street in self.all_nodes:
            self.update_street_lines(self.all_nodes[id_street], id_street)

    def nearest_node_order(self, nodes):
        if not nodes:
            return []
        
        ordered_nodes = [nodes.pop(0)]
        current_node = ordered_nodes[0]

        while nodes:
            nearest_node = min(nodes, key=lambda node: haversine(current_node[0], current_node[1], node[0], node[1]))
            ordered_nodes.append(nearest_node)
            nodes.remove(nearest_node)
            current_node = nearest_node
        
        return ordered_nodes
    
    def near_street(self, x, y):
        closest_id_street = None
        closest_distance = float('inf')

        for id_street, line in self.lines.items():
            line_points = line.points

            distance = self.get_distance_to_line(x, y, line_points)

            if distance < closest_distance:
                closest_distance = distance
                closest_id_street = id_street

        return closest_id_street 


    def get_distance_to_line(self, x, y, line_points):
        min_distance = float('inf')

        for i in range(0, len(line_points), 2):
            start = (line_points[i], line_points[i + 1])
            end = (line_points[i + 2], line_points[i + 3]) 

            distance = distance_to_segment((x, y), start, end)
            if distance < min_distance:
                min_distance = distance

            if (i+3) == len(line_points) - 1:
                break

        return min_distance
    
    def schedule_update(self, *args):
        self.trigger_update_street_lines()

    def add_street(self, nodes, id_street):
        self.nodes = self.nearest_node_order(nodes)
        self.id_street = id_street
        if self.id_street in self.all_nodes:
            pass
        else:
            self.all_nodes[id_street] = self.nodes
        
        self.draw_street()

    def get_window_xy(self, lat, lon):
        height = self.map_view.height
        width = self.map_view.width

        lat0, lon0, lat100, lon100 = self.map_view.get_bbox(0)
        if lat100 == lat0:
            return 0,0

        m_lat = height / (lat100 - lat0)

        if lon100 == lon0:
            return 0,0
        m_lon = width / (lon100 - lon0)

        n_lat = (m_lat)*lat0
        n_lon = (m_lon)*lon0

        y = m_lat * lat - n_lat
        x = m_lon * lon - n_lon

        return x,y



