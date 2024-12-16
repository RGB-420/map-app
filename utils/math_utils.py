import math

# Haversine formula to calculate the distance between two points on Earth
def haversine(lon1, lat1, lon2, lat2):
    # Radius of the Earth in meters
    R = 6371000
    
    # Convert the coordinates from degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in meters
    distance = R * c
    
    return distance

# Function to calculate the shortest distance from a point to a line segment
def distance_to_segment(point, start, end):
    px, py = point  # Point coordinates
    x1, y1 = start  # Start point coordinates of the segment
    x2, y2 = end    # End point coordinates of the segment

    # Differences between the end and start points
    dx = x2 - x1
    dy = y2 - y1

    # If the start and end points are the same, return the distance to that point
    if dx == 0 and dy == 0:
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

    # Calculate the projection factor t of the point onto the line segment
    t = ((px - x1) * dx + (py - y1) * dy) / (dx ** 2 + dy ** 2)

    # Clamp t to the range [0, 1] to ensure the closest point is on the segment
    t = max(0, min(1, t))

    # Calculate the coordinates of the closest point on the segment
    close_x = x1 + t * dx
    close_y = y1 + t * dy

    # Distance from the point to the closest point on the segment
    distance = math.sqrt((px - close_x) ** 2 + (py - close_y) ** 2)

    return distance