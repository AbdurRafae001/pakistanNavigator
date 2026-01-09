import csv
from math import radians, sin, cos, sqrt, atan2

# Haversine distance function (km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Load city data (or embed directly)
cities = []
with open("pak_cities.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cities.append({
            "name": row["City"],
            "lat": float(row["Latitude"]),
            "lon": float(row["Longitude"])
        })

# Build edges based on threshold
threshold_km = 200
edges = []
n = len(cities)
for i in range(n):
    for j in range(i+1, n):
        d = haversine(cities[i]["lat"], cities[i]["lon"],
                      cities[j]["lat"], cities[j]["lon"])
        if d <= threshold_km:
            edges.append((cities[i]["name"], cities[j]["name"], round(d,1)))

# Example: print edges
for u, v, dist in edges:
    print(f"{u} — {v} : {dist} km")

# Build adjacency list (undirected)
adj = { city["name"]: [] for city in cities }
for u, v, dist in edges:
    adj[u].append((v, dist))
    adj[v].append((u, dist))

# Print adjacency list
for city, neigh in adj.items():
    print(city, ":", neigh)
