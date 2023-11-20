import matplotlib.pyplot as plt
import networkx as nx
import heapq

# Function to find the shortest path using Dijkstra's algorithm
def dijkstra(graph, start_node):
    # Initialize distance dictionary with infinity values for all nodes except the start node
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    
    # Priority queue to store nodes and their corresponding distances
    priority_queue = [(0, start_node)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Ignore if the current distance is greater than the stored distance for the current node
        if current_distance > distances[current_node]:
            continue
        
        # Explore neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # Update the distance if a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

# Sample network topology represented as a graph
graph = {
    'Router1': {'Switch1': 5, 'Switch2': 3},
    'Switch1': {'Server1': 2},
    'Switch2': {'Switch1': 1, 'Server1': 1},
    'Server1': {'Router1': 1, 'Printer1': 3},
    'Printer1': {'Switch1': 2}
}

start_node = 'Router1'
shortest_distances = dijkstra(graph, start_node)

# Create a graph using networkx library
G = nx.Graph()
for node, edges in graph.items():
    for neighbor, weight in edges.items():
        G.add_edge(node, neighbor, weight=weight)

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Draw the graph
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, ax=ax, with_labels=False, node_color='blue', node_size=500, font_color='white')

# Draw the edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

# Draw the precise variable names as labels
node_labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax, font_color='red')

# Set the plot title
ax.set_title("Network Topology")

# Adjust the plot layout
plt.tight_layout()

# Display the plot
plt.show()