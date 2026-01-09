# 🇵🇰 Pakistan Shortest Path Finder

A practical route planner for finding the shortest path between Pakistani cities using **Dijkstra's Algorithm**.

**Course:** Design and Analysis of Algorithms (DAA)  
**Semester:** Fall 2025

---

## 📋 Project Overview

This project implements a complete route planning system in three phases:

1. **Phase 1: Data Preparation** - Filter world cities dataset for Pakistani cities
2. **Phase 2: Algorithm Implementation** - Dijkstra's shortest path algorithm from scratch
3. **Phase 3: Web Interface** - Interactive Streamlit application

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare the Data

Run the data preparation script to filter Pakistani cities:

```bash
python data_preparation.py
```

This creates `pak_cities.csv` with filtered Pakistani cities.

### 3. Launch the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
algo_project/
├── data_preparation.py      # Phase 1: Data filtering
├── dijkstra.py              # Phase 2: Algorithm implementation
├── app.py                   # Phase 3: Streamlit web app
├── pak_cities.csv           # Generated: Filtered Pakistani cities
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── simplemaps_worldcities_basicv1.901/
    └── worldcities.csv     # Source dataset
```

---

## 🔧 How It Works

### Phase 1: Data Preparation
- Loads the world cities dataset (48,000+ cities)
- Filters for cities where `country == 'Pakistan'`
- Extracts: City Name, Latitude, Longitude
- Saves to `pak_cities.csv`

### Phase 2: Dijkstra's Algorithm
- **Graph Construction**: Each city is a node; edges connect cities within a distance threshold
- **Distance Calculation**: Uses the Haversine formula for great-circle distance
- **Algorithm**: Implemented from scratch using a min-heap priority queue
- **Output**: Returns the shortest path and total distance in kilometers

### Phase 3: Web Application
- Two dropdown menus for source and destination cities
- Configurable edge distance threshold
- Visual display of the route and statistics
- Detailed step-by-step route breakdown

---

## 📊 Algorithm Details

### Haversine Formula
Calculates the great-circle distance between two points on Earth:

```python
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × asin(√a)
distance = R × c  # R = 6371 km (Earth's radius)
```

### Dijkstra's Algorithm
1. Initialize all distances to infinity except source (0)
2. Use a priority queue to process cities by minimum distance
3. For each city, update neighbor distances if a shorter path is found
4. Reconstruct path by backtracking from destination to source

**Time Complexity:** O((V + E) log V) where V = cities, E = edges

---

## 🧪 Testing the Algorithm

Run the algorithm module directly to test:

```bash
python dijkstra.py
```

This tests paths like:
- Karachi → Lahore
- Islamabad → Peshawar

---

## 📝 Notes

- The default edge threshold is 300 km (adjustable in the app)
- Increase the threshold if no path is found between distant cities
- The algorithm guarantees the shortest path for positive edge weights

---

## 📚 References

- [Dijkstra's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Haversine Formula](https://en.wikipedia.org/wiki/Haversine_formula)
- [SimpleMaps World Cities Database](https://simplemaps.com/data/world-cities)

---

**Built with ❤️ for DAA Fall 2025**

