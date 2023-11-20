import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

def create_network_graph(nodes_data, edges_data):
    G = nx.Graph()
    G.add_nodes_from(nodes_data)
    G.add_weighted_edges_from(edges_data)
    return G

def display_network_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray', width=1.5, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Network Graph")
    plt.axis('off')

def display_shortest_path(source, target, G):
    path = nx.shortest_path(G, source=source, target=target)
    distance = nx.shortest_path_length(G, source=source, target=target)
    message = f"Shortest Path from {source} to {target}: {path}\nDistance: {distance}"
    messagebox.showinfo("Shortest Path", message)

def add_node():
    name = node_name_entry.get()
    node_type = node_type_combobox.get()
    node_info = node_info_entry.get()
    G.add_node(name, type=node_type, info=node_info)
    node_name_entry.delete(0, tk.END)
    node_type_combobox.set('')
    node_info_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Network Graph Visualization")

# Create a figure for the network graph
fig, ax = plt.subplots(figsize=(8, 6))

# Create a canvas for the network graph figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a frame for the node options
options_frame = ttk.Frame(root)
options_frame.pack(side=tk.TOP, pady=10)

# Create labels and entry fields for node information
node_name_label = ttk.Label(options_frame, text="Node Name:")
node_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

node_name_entry = ttk.Entry(options_frame)
node_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

node_type_label = ttk.Label(options_frame, text="Node Type:")
node_type_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

node_type_combobox = ttk.Combobox(options_frame, values=['router', 'switch', 'server'])
node_type_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

node_info_label = ttk.Label(options_frame, text="Node Info:")
node_info_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

node_info_entry = ttk.Entry(options_frame)
node_info_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

add_node_button = ttk.Button(options_frame, text="Add Node", command=add_node)
add_node_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Define the nodes and edges of the network graph
nodes_data = [('router1', {'type': 'router', 'info': 'Router 1'}),
              ('switch1', {'type': 'switch', 'info': 'Switch 1'}),
              ('server1', {'type': 'server', 'info': 'Server 1'})]
edges_data = [('router1', 'switch1', {'weight': 2}),
              ('switch1', 'server1', {'weight': 1})]
G = create_network_graph(nodes_data, edges_data)

# Display the network graph
display_network_graph(G)

# Start the Tkinter event loop
root.mainloop()
