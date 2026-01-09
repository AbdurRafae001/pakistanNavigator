"""
Comprehensive Pakistan Locations Database
Includes cities, areas, neighborhoods, landmarks, and points of interest
"""

# Major city areas and neighborhoods
KARACHI_AREAS = {
    "DHA Karachi": (24.8138, 67.0304),
    "Clifton Karachi": (24.8093, 67.0311),
    "Gulshan-e-Iqbal": (24.9214, 67.0931),
    "North Nazimabad": (24.9425, 67.0344),
    "Saddar Karachi": (24.8556, 67.0228),
    "Korangi": (24.8422, 67.1308),
    "PECHS Karachi": (24.8700, 67.0700),
    "Malir": (24.8903, 67.1983),
    "Gulistan-e-Jauhar": (24.9275, 67.1167),
    "FB Area Karachi": (24.9214, 67.0556),
    "Nazimabad": (24.9119, 67.0344),
    "Liaquatabad": (24.8983, 67.0253),
    "Tariq Road": (24.8700, 67.0600),
    "Bahadurabad": (24.8800, 67.0800),
    "Garden Karachi": (24.8650, 67.0350),
    "Jinnah Airport Karachi": (24.9065, 67.1608),
    "Port Qasim": (24.7833, 67.3500),
    "Kemari": (24.8333, 66.9833),
}

LAHORE_AREAS = {
    "DHA Lahore": (31.4697, 74.4228),
    "Gulberg Lahore": (31.5150, 74.3461),
    "Model Town Lahore": (31.4833, 74.3167),
    "Johar Town": (31.4697, 74.2697),
    "Bahria Town Lahore": (31.3667, 74.1833),
    "Cantt Lahore": (31.5394, 74.3586),
    "Mall Road Lahore": (31.5600, 74.3300),
    "Anarkali": (31.5700, 74.3200),
    "Liberty Market": (31.5150, 74.3461),
    "Faisal Town Lahore": (31.4833, 74.3000),
    "Township Lahore": (31.4500, 74.3000),
    "Iqbal Town Lahore": (31.5000, 74.2833),
    "Wapda Town Lahore": (31.4500, 74.2667),
    "Valencia Town": (31.4333, 74.2500),
    "Allama Iqbal Airport": (31.5216, 74.4036),
    "Data Darbar": (31.5700, 74.3100),
    "Badshahi Mosque": (31.5881, 74.3106),
    "Minar-e-Pakistan": (31.5925, 74.3092),
}

ISLAMABAD_AREAS = {
    "F-6 Islamabad": (33.7294, 73.0931),
    "F-7 Islamabad": (33.7200, 73.0700),
    "F-8 Islamabad": (33.7100, 73.0500),
    "F-10 Islamabad": (33.6900, 73.0200),
    "F-11 Islamabad": (33.6800, 73.0000),
    "G-9 Islamabad": (33.6900, 73.0400),
    "G-10 Islamabad": (33.6700, 73.0200),
    "G-11 Islamabad": (33.6600, 73.0000),
    "Blue Area Islamabad": (33.7100, 73.0600),
    "E-11 Islamabad": (33.6800, 72.9800),
    "I-8 Islamabad": (33.6600, 73.0800),
    "I-10 Islamabad": (33.6400, 73.0600),
    "DHA Islamabad": (33.5200, 73.1500),
    "Bahria Town Islamabad": (33.5500, 73.1200),
    "Faisal Mosque": (33.7297, 73.0372),
    "Pakistan Monument": (33.6931, 73.0689),
    "Centaurus Mall": (33.7081, 73.0508),
    "Islamabad Airport": (33.5606, 72.8495),
    "Daman-e-Koh": (33.7419, 73.0619),
    "Margalla Hills": (33.7500, 73.0500),
    "Saidpur Village": (33.7433, 73.0650),
}

RAWALPINDI_AREAS = {
    "Saddar Rawalpindi": (33.5969, 73.0528),
    "Commercial Market Rawalpindi": (33.5950, 73.0500),
    "Satellite Town Rawalpindi": (33.6100, 73.0700),
    "Bahria Town Rawalpindi": (33.5167, 73.1333),
    "Chaklala": (33.5600, 73.1000),
    "Westridge": (33.5800, 73.0600),
    "Rawalpindi Cantt": (33.5700, 73.0700),
    "Raja Bazaar": (33.6000, 73.0600),
    "Committee Chowk": (33.6000, 73.0550),
    "Shamsabad": (33.5900, 73.0800),
    "Adiala Road": (33.5500, 73.0200),
}

PESHAWAR_AREAS = {
    "Hayatabad": (33.9800, 71.4300),
    "University Town Peshawar": (34.0100, 71.5200),
    "Saddar Peshawar": (34.0100, 71.5700),
    "Cantt Peshawar": (34.0000, 71.5500),
    "Gulbahar": (34.0200, 71.5600),
    "Board Bazaar": (34.0100, 71.5800),
    "Qissa Khwani Bazaar": (34.0128, 71.5772),
    "Bala Hisar Fort": (34.0097, 71.5822),
    "Peshawar Airport": (33.9939, 71.5147),
}

QUETTA_AREAS = {
    "Cantt Quetta": (30.2000, 67.0100),
    "Satellite Town Quetta": (30.1800, 67.0200),
    "Jinnah Road Quetta": (30.1900, 66.9900),
    "Alamdar Road": (30.1700, 67.0000),
    "Brewery Road": (30.1950, 67.0050),
    "Zarghoon Road": (30.1850, 67.0100),
    "Quetta Airport": (30.2514, 66.9375),
}

MULTAN_AREAS = {
    "Cantt Multan": (30.1800, 71.4500),
    "Bosan Road": (30.2000, 71.4300),
    "Gulgasht Colony": (30.2100, 71.4400),
    "Shah Rukn-e-Alam Shrine": (30.1956, 71.4756),
    "Hussain Agahi": (30.2000, 71.4700),
    "Multan Airport": (30.2033, 71.4192),
}

FAISALABAD_AREAS = {
    "D Ground Faisalabad": (31.4200, 73.1000),
    "Peoples Colony": (31.4300, 73.0800),
    "Madina Town": (31.4100, 73.0700),
    "Gulberg Faisalabad": (31.4000, 73.1100),
    "Jaranwala Road": (31.4200, 73.1200),
    "Clock Tower": (31.4167, 73.0833),
    "Faisalabad Airport": (31.3650, 72.9950),
}

# Famous landmarks and tourist spots
LANDMARKS = {
    "Badshahi Mosque Lahore": (31.5881, 74.3106),
    "Faisal Mosque Islamabad": (33.7297, 73.0372),
    "Minar-e-Pakistan": (31.5925, 74.3092),
    "Pakistan Monument": (33.6931, 73.0689),
    "Quaid-e-Azam Mausoleum": (24.8752, 67.0409),
    "Lahore Fort": (31.5881, 74.3158),
    "Shalimar Gardens": (31.5858, 74.3817),
    "Mohatta Palace": (24.8100, 67.0300),
    "Frere Hall Karachi": (24.8500, 67.0300),
    "K2 Base Camp": (35.8825, 76.5133),
    "Hunza Valley": (36.3167, 74.6500),
    "Swat Valley": (35.2227, 72.3531),
    "Naran Kaghan": (34.9000, 73.6500),
    "Murree": (33.9070, 73.3943),
    "Nathia Gali": (34.0667, 73.3833),
    "Ayubia National Park": (34.0500, 73.4000),
    "Taxila Museum": (33.7465, 72.7861),
    "Mohenjo-daro": (27.3242, 68.1386),
    "Rohtas Fort": (32.9667, 73.5833),
    "Derawar Fort": (28.7583, 71.3417),
    "Fairy Meadows": (35.4167, 74.6000),
    "Lake Saif ul Malook": (34.8772, 73.6906),
    "Attabad Lake": (36.3333, 74.8500),
    "Khunjerab Pass": (36.8500, 75.4167),
}

# Airports
AIRPORTS = {
    "Jinnah International Airport Karachi": (24.9065, 67.1608),
    "Allama Iqbal Airport Lahore": (31.5216, 74.4036),
    "Islamabad International Airport": (33.5606, 72.8495),
    "Bacha Khan Airport Peshawar": (33.9939, 71.5147),
    "Quetta International Airport": (30.2514, 66.9375),
    "Multan International Airport": (30.2033, 71.4192),
    "Faisalabad Airport": (31.3650, 72.9950),
    "Sialkot Airport": (32.5356, 74.3639),
    "Skardu Airport": (35.3356, 75.5364),
    "Gilgit Airport": (35.9189, 74.3336),
}

# Bus Terminals
BUS_TERMINALS = {
    "Daewoo Terminal Karachi": (24.8700, 67.0600),
    "Daewoo Terminal Lahore": (31.5500, 74.3400),
    "Daewoo Terminal Islamabad": (33.6600, 73.0400),
    "Faisal Movers Lahore": (31.5450, 74.3350),
    "Faisal Movers Islamabad": (33.6550, 73.0350),
    "Niazi Express Karachi": (24.8750, 67.0650),
}

# Railway Stations
RAILWAY_STATIONS = {
    "Karachi City Station": (24.8514, 67.0311),
    "Karachi Cantt Station": (24.8556, 67.0644),
    "Lahore Junction": (31.5778, 74.3056),
    "Rawalpindi Railway Station": (33.6000, 73.0556),
    "Peshawar Cantt Station": (34.0042, 71.5444),
    "Quetta Railway Station": (30.1833, 66.9917),
    "Multan Cantt Station": (30.1833, 71.4500),
    "Faisalabad Railway Station": (31.4167, 73.0833),
}

# Universities
UNIVERSITIES = {
    "LUMS Lahore": (31.4697, 74.4089),
    "NUST Islamabad": (33.6425, 72.9903),
    "FAST Karachi": (24.9147, 67.0900),
    "FAST Lahore": (31.5167, 74.3833),
    "FAST Islamabad": (33.6597, 73.0058),
    "IBA Karachi": (24.9456, 67.1161),
    "UET Lahore": (31.5744, 74.3569),
    "NED Karachi": (24.9339, 67.1117),
    "Punjab University": (31.5028, 74.3017),
    "Quaid-e-Azam University": (33.7472, 73.1372),
    "COMSATS Islamabad": (33.6528, 73.0275),
    "Peshawar University": (34.0167, 71.5667),
    "Karachi University": (24.9417, 67.1200),
    "Agha Khan University": (24.8933, 67.0744),
}

# Hospitals
HOSPITALS = {
    "Agha Khan Hospital Karachi": (24.8933, 67.0744),
    "Jinnah Hospital Karachi": (24.8833, 67.0417),
    "Shaukat Khanum Lahore": (31.4833, 74.4167),
    "Mayo Hospital Lahore": (31.5722, 74.3222),
    "PIMS Islamabad": (33.7044, 73.0506),
    "Shifa Hospital Islamabad": (33.6842, 73.0514),
    "CMH Rawalpindi": (33.5833, 73.0667),
    "Lady Reading Hospital Peshawar": (34.0167, 71.5667),
}

def get_all_locations():
    """Combine all locations into a single dictionary."""
    all_locations = {}
    
    # Add city areas
    all_locations.update(KARACHI_AREAS)
    all_locations.update(LAHORE_AREAS)
    all_locations.update(ISLAMABAD_AREAS)
    all_locations.update(RAWALPINDI_AREAS)
    all_locations.update(PESHAWAR_AREAS)
    all_locations.update(QUETTA_AREAS)
    all_locations.update(MULTAN_AREAS)
    all_locations.update(FAISALABAD_AREAS)
    
    # Add landmarks
    all_locations.update(LANDMARKS)
    
    # Add transport hubs
    all_locations.update(AIRPORTS)
    all_locations.update(BUS_TERMINALS)
    all_locations.update(RAILWAY_STATIONS)
    
    # Add institutions
    all_locations.update(UNIVERSITIES)
    all_locations.update(HOSPITALS)
    
    return all_locations


def get_location_categories():
    """Return locations grouped by category."""
    return {
        "🏙️ Karachi Areas": list(KARACHI_AREAS.keys()),
        "🏙️ Lahore Areas": list(LAHORE_AREAS.keys()),
        "🏙️ Islamabad Areas": list(ISLAMABAD_AREAS.keys()),
        "🏙️ Rawalpindi Areas": list(RAWALPINDI_AREAS.keys()),
        "🏙️ Peshawar Areas": list(PESHAWAR_AREAS.keys()),
        "🏙️ Quetta Areas": list(QUETTA_AREAS.keys()),
        "🏙️ Multan Areas": list(MULTAN_AREAS.keys()),
        "🏙️ Faisalabad Areas": list(FAISALABAD_AREAS.keys()),
        "🏛️ Landmarks & Tourist Spots": list(LANDMARKS.keys()),
        "✈️ Airports": list(AIRPORTS.keys()),
        "🚌 Bus Terminals": list(BUS_TERMINALS.keys()),
        "🚂 Railway Stations": list(RAILWAY_STATIONS.keys()),
        "🎓 Universities": list(UNIVERSITIES.keys()),
        "🏥 Hospitals": list(HOSPITALS.keys()),
    }

