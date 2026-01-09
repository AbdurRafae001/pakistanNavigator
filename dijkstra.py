"""
Phase 2: Dijkstra's Algorithm Implementation
Implements the shortest path algorithm from scratch for Pakistani cities.
"""

import math
import csv
import heapq


def calculate_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth 
    using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
    
    Returns:
        Distance in kilometers (float)
    """
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Compute differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Earth's radius in kilometers
    R = 6371  

    # Total distance
    distance = R * c
    return distance


def load_cities(filepath):
    """
    Load Pakistani cities from CSV file.
    
    Args:
        filepath: Path to pak_cities.csv
    
    Returns:
        List of city dictionaries with name, lat, lon
    """
    cities = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cities.append({
                "name": row["City"],
                "lat": float(row["Latitude"]),
                "lon": float(row["Longitude"])
            })
    return cities


def build_graph(cities, threshold_km=300):
    """
    Build a weighted graph connecting nearby cities.
    
    Args:
        cities: List of city dictionaries
        threshold_km: Maximum distance (km) to create an edge between cities
    
    Returns:
        adjacency_list: Dictionary mapping each city to list of (neighbor, distance) tuples
    """
    n = len(cities)
    
    # Initialize adjacency list
    adjacency_list = {city["name"]: [] for city in cities}
    
    # Calculate edges between all city pairs within threshold
    for i in range(n):
        for j in range(i + 1, n):
            distance = calculate_distance_km(
                cities[i]["lat"], cities[i]["lon"],
                cities[j]["lat"], cities[j]["lon"]
            )
            
            if distance <= threshold_km:
                # Add edge in both directions (undirected graph)
                adjacency_list[cities[i]["name"]].append((cities[j]["name"], round(distance, 2)))
                adjacency_list[cities[j]["name"]].append((cities[i]["name"], round(distance, 2)))
    
    return adjacency_list


def dijkstra(adjacency_list, source, destination):
    """
    Dijkstra's Algorithm Implementation from Scratch.
    
    Finds the shortest path between source and destination cities.
    
    Args:
        adjacency_list: Graph represented as adjacency list
        source: Starting city name
        destination: Ending city name
    
    Returns:
        tuple: (path, total_distance)
            - path: List of cities in the shortest path
            - total_distance: Total distance in kilometers
            Returns (None, float('inf')) if no path exists
    """
    # Validate input cities exist in graph
    if source not in adjacency_list:
        raise ValueError(f"Source city '{source}' not found in graph")
    if destination not in adjacency_list:
        raise ValueError(f"Destination city '{destination}' not found in graph")
    
    # Initialize distances to infinity for all cities
    distances = {city: float('inf') for city in adjacency_list}
    distances[source] = 0
    
    # Track the previous city in the shortest path (for path reconstruction)
    previous = {city: None for city in adjacency_list}
    
    # Track visited cities
    visited = set()
    
    # Priority queue: (distance, city)
    # Using min-heap to always process the city with smallest distance first
    priority_queue = [(0, source)]
    
    while priority_queue:
        # Extract city with minimum distance
        current_distance, current_city = heapq.heappop(priority_queue)
        
        # Skip if already visited
        if current_city in visited:
            continue
        
        # Mark as visited
        visited.add(current_city)
        
        # If we reached destination, we can stop
        if current_city == destination:
            break
        
        # Explore all neighbors of current city
        for neighbor, edge_weight in adjacency_list[current_city]:
            if neighbor in visited:
                continue
            
            # Calculate new distance through current city
            new_distance = current_distance + edge_weight
            
            # If this path is shorter, update the distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_city
                heapq.heappush(priority_queue, (new_distance, neighbor))
    
    # Reconstruct the path from destination to source
    if distances[destination] == float('inf'):
        # No path exists
        return None, float('inf')
    
    # Build path by backtracking from destination
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    
    # Reverse to get path from source to destination
    path.reverse()
    
    return path, round(distances[destination], 2)


def get_all_cities(filepath):
    """
    Get list of all city names from the dataset.
    
    Args:
        filepath: Path to pak_cities.csv
    
    Returns:
        Sorted list of city names
    """
    cities = load_cities(filepath)
    return sorted([city["name"] for city in cities])


# Main execution for testing
if __name__ == "__main__":
    # Load cities
    print("Loading Pakistani cities...")
    cities = load_cities("pak_cities.csv")
    print(f"Loaded {len(cities)} cities")
    
    # Build graph
    print("\nBuilding graph with 300km threshold...")
    graph = build_graph(cities, threshold_km=300)
    
    # Count total edges
    total_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    print(f"Total edges in graph: {total_edges}")
    
    # Test Dijkstra's algorithm
    print("\n" + "="*50)
    print("Testing Dijkstra's Algorithm")
    print("="*50)
    
    # Test case 1: Karachi to Lahore
    source = "Karachi"
    destination = "Lahore"
    
    print(f"\nFinding shortest path: {source} → {destination}")
    path, distance = dijkstra(graph, source, destination)
    
    if path:
        print(f"Shortest Path: {' → '.join(path)}")
        print(f"Total Distance: {distance} km")
    else:
        print("No path found between these cities!")
    
    # Test case 2: Islamabad to Peshawar
    source2 = "Islamabad"
    destination2 = "Peshawar"
    
    print(f"\nFinding shortest path: {source2} → {destination2}")
    path2, distance2 = dijkstra(graph, source2, destination2)
    
    if path2:
        print(f"Shortest Path: {' → '.join(path2)}")
        print(f"Total Distance: {distance2} km")
    else:
        print("No path found between these cities!")

