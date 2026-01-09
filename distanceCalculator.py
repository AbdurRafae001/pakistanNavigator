import math

def calculate_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth 
    specified by their latitude and longitude using the Haversine formula.

    Returns:
        Distance in kilometers (float)
    """

    # Step 1: Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Step 2: Compute differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Step 3: Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Step 4: Earth’s radius in kilometers
    R = 6371  

    # Step 5: Total distance
    distance = R * c
    return distance


dist = calculate_distance_km(24.86, 67.01, 34.0144,71.5675)
print("Distance:", dist, "km")

