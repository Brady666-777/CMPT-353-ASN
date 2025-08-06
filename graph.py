import networkx as nx
import matplotlib.pyplot as plt

# Define the devices and their types
devices = {
    1: "Laptop",
    2: "Tablet",
    3: "Smartphone",
    4: "Laptop",
    5: "Tablet",
    6: "Smartphone",
    7: "Smartphone",
    8: "Laptop",
    9: "Smartphone",
    10: "Smartphone"
}

# Define the connections (edges) between devices
# These are assumed based on a typical network diagram
# Update connections to match the diagram
connections = [
    (1, 4), (2, 4), (3, 4), (4, 5), (5, 6), (5, 7), (5, 8), (8, 9), (8, 10)
]

# Create a graph
G = nx.Graph()

# Add nodes with device type as attribute
for device_id, device_type in devices.items():
    G.add_node(device_id, device_type=device_type)

# Add edges
G.add_edges_from(connections)

# Define colors for different device types
color_map = {
    "Laptop": "skyblue",
    "Tablet": "lightgreen",
    "Smartphone": "lightcoral"
}
node_colors = [color_map[G.nodes[node]['device_type']] for node in G.nodes]

# Manually set positions to match the diagram layout
pos = {
    1: (0, 2),    # Laptop top left
    2: (-2, 0),   # Tablet far left
    3: (0, -2),   # Smartphone bottom left
    4: (0, 0),    # Laptop center left
    5: (3, 0),    # Tablet center right (thicker border in image)
    6: (3, 2),    # Smartphone top right
    7: (3, -2),   # Smartphone bottom right
    8: (5, 0),    # Laptop far right
    9: (7, 2),    # Smartphone top far right
    10: (7, -2)   # Smartphone bottom far right
}

# Draw the graph
plt.figure(figsize=(10, 5))
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_weight='bold', edge_color='gray', style='dashed')

# Create legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, label=label) for label, color in color_map.items()]
plt.legend(handles=legend_elements, title="Device Types")

plt.title("Wireless Network Diagram")
plt.axis('off')
plt.show()

