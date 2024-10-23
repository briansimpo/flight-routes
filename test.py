
# Setting up the graph based on the given image
from algorithm import Graph


airports = {
    "DSM": 0, "ORD": 1, "BGI": 2, "LGA": 3, "TLV": 4, "DEL": 5, "DOH": 6, "CDG": 7, "SIN": 8, 
    "BUD": 9, "JFK": 10, "HND": 11, "ICN": 12, "SFO": 13, "SAN": 14, "EYW": 15, "LHR": 16, "EWR": 17
}


# Routes based on the image
routes = [
    ("DSM", "ORD"), ("ORD", "BGI"), ("BGI", "LGA"), ("LGA", "ORD"), 
    ("TLV", "DEL"), ("DEL", "CDG"), ("CDG", "BUD"), ("CDG", "DEL"), ("CDG", "SIN"), ("SIN", "CDG"), 
    ("DEL", "DOH"), ("JFK", "HND"), ("HND", "ICN"), ("ICN", "JFK"), 
    ("SFO", "SAN"), ("SAN", "EYW"), ("EYW", "SFO"), ("SFO", "LHR"), ("LHR", "SFO"), ("EWR", "HND")
]

# Instantiate the graph
graph = Graph(airports)
graph.add_routes(routes)

# Example: Find minimum number of additional routes needed from TLV
start_airport = "DSM"
additional_routes_needed = graph.find_minimum_additional_routes(start_airport)

print(f"Minimum number of additional routes needed from {start_airport}: {additional_routes_needed}")


