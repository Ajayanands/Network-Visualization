import tkinter as tk
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory

# Create a sample network graph with weighted edges
def create_network_graph():
    G = nx.Graph()
    G.add_nodes_from([
        ('Router 1', {'type': 'router', 'info': 'IP: 192.168.0.1'}),
        ('Router 2', {'type': 'router', 'info': 'IP: 192.168.0.2'}),
        ('Switch 1', {'type': 'switch', 'info': 'Status: Online'}),
        ('Switch 2', {'type': 'switch', 'info': 'Status: Online'}),
        ('Server 1', {'type': 'server', 'info': 'IP: 192.168.0.10'}),
        ('Server 2', {'type': 'server', 'info': 'IP: 192.168.0.11'})
    ])
    G.add_weighted_edges_from([
        ('Router 1', 'Switch 1', 3),
        ('Router 1', 'Switch 2', 5),
        ('Router 2', 'Switch 2', 2),
        ('Switch 1', 'Server 1', 4),
        ('Switch 2', 'Server 2', 6)
    ])
    return G

# Function to find the shortest path from a source node to all other nodes
def find_shortest_path(source_node, G):
    shortest_paths = nx.shortest_path(G, source=source_node, weight='weight')
    return shortest_paths

# Function to display the shortest path from a source node to a target node
def display_shortest_path(source_node, target_node, G):
    shortest_path = nx.shortest_path(G, source=source_node, target=target_node, weight='weight')
    path_text = ' -> '.join(shortest_path)
    messagebox.showinfo("Shortest Path", f"The shortest path from {source_node} to {target_node} is:\n{path_text}")

# Create the main window
window = tk.Tk()
window.title("Network Visualization")

# Create a frame for the graph display
graph_frame = tk.Frame(window)
graph_frame.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame for the options
options_frame = tk.Frame(window)
options_frame.pack(side=tk.RIGHT, padx=5, pady=5)

# Create a graph figure and canvas
figure = plt.figure(figsize=(8, 6))
ax = figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Function to display the network graph
def display_network_graph(pos=None):
    G = create_network_graph()
    if pos is None:
        pos = nx.spring_layout(G)  # Use spring layout as default

    # Clear the plot
    ax.clear()

    # Draw routers
    routers = [node for node in G.nodes if G.nodes[node]['type'] == 'router']
    nx.draw_networkx_nodes(G, pos, nodelist=routers, ax=ax, node_color='lightblue', node_size=800, node_shape='s')

    # Draw switches
    switches = [node for node in G.nodes if G.nodes[node]['type'] == 'switch']
    nx.draw_networkx_nodes(G, pos, nodelist=switches, ax=ax, node_color='lightgreen', node_size=800, node_shape='^')

    # Draw servers
    servers = [node for node in G.nodes if G.nodes[node]['type'] == 'server']
    nx.draw_networkx_nodes(G, pos, nodelist=servers, ax=ax, node_color='lightpink', node_size=800, node_shape='o')

    # Draw edges with weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edges(G, pos, ax=ax, width=2.0, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    # Set node labels
    node_labels = nx.get_node_attributes(G, 'info')
    nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax, font_size=8)

    # Set plot title
    ax.set_title('Network Graph')

    # Refresh canvas
    canvas.draw()

# Display the network graph
display_network_graph()

# Create a frame to hold the comboboxes
combobox_frame = tk.Frame(options_frame)
combobox_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create the GUI elements inside the combobox frame
source_label = ttk.Label(combobox_frame , text="Source Node:")
source_label.pack(side=tk.LEFT, padx=5, pady=5)
source_combobox = ttk.Combobox(combobox_frame , values=list(create_network_graph().nodes()), width=15)
source_combobox.pack(side=tk.LEFT, padx=5, pady=5)

target_label = ttk.Label(combobox_frame , text="Target Node:")
target_label.pack(side=tk.LEFT, padx=5, pady=5)
target_combobox = ttk.Combobox(combobox_frame , values=list(create_network_graph().nodes()), width=15)
target_combobox.pack(side=tk.LEFT, padx=5, pady=5)

shortest_path_button = ttk.Button(combobox_frame , text="Find Shortest Path", command=lambda: display_shortest_path(source_combobox.get(), target_combobox.get(), create_network_graph()))
shortest_path_button.pack(side=tk.LEFT, padx=5, pady=5)

def get_node_icon(node_type):
    if node_type == 'router':
        return ('s', 'Square')  # Square shape
    elif node_type == 'switch':
        return ('^', 'Triangle')  # Triangle shape
    elif node_type == 'server':
        return ('o', 'Circle')  # Circle shape
    else:
        return ('N/A', 'Unknown')  # Return 'N/A' for unknown types

def display_node_info():
    node_name = node_combobox.get()
    if node_name:
        G = create_network_graph()
        node_info = G.nodes[node_name]['info']
        node_type = G.nodes[node_name]['type']
        node_icon, node_shape = get_node_icon(node_type)

        messagebox.showinfo(f"{node_name} Information", f"Node Shape: {node_shape}\n\nNode Icon: {node_icon}\n\n{node_info}")

# Create the combobox for node selection
node_combobox = ttk.Combobox(options_frame, values=list(create_network_graph().nodes()), width=15)
node_combobox.pack(side=tk.TOP, padx=5, pady=5)

# Add the button to display node information
node_button = ttk.Button(options_frame , text="Node Info", command=display_node_info)
node_button.pack(side=tk.TOP, padx=5, pady=5)

original_pos = nx.spring_layout(create_network_graph())

def switch_layout(layout):
    G = create_network_graph()
    pos = None
    if layout == "spring":
        pos = nx.spring_layout(G)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "hierarchical":
        pos = nx.kamada_kawai_layout(G)
    elif layout == "original":
        pos = original_pos
        display_network_graph(pos)  # Call the display_network_graph function with the original layout
        return
    # Clear the plot
    ax.clear()

    # Draw the graph with the selected layout
    nx.draw_networkx(G, pos, ax=ax)

    # Refresh canvas
    canvas.draw()

# Add a combobox for layout selection
layout_combobox = ttk.Combobox(options_frame, values=["spring", "circular", "hierarchical", "original"], width=15)
layout_combobox.pack(side=tk.TOP, padx=5, pady=5)
layout_combobox.set("spring")  # Set the default layout

# Add a button to apply the selected layout
layout_button = ttk.Button(options_frame, text="Apply Layout", command=lambda: switch_layout(layout_combobox.get()))
layout_button.pack(side=tk.TOP, padx=5, pady=5)

def export_graph(file_path, file_format):
    canvas.figure.savefig(file_path, format=file_format)

# Create a frame for export options
export_frame = tk.Frame(options_frame)
export_frame.pack(side=tk.TOP, padx=5, pady=5)

# Function to open the file explorer and select a file path
def browse_file():
    file_path = askdirectory()
    file_path_entry.delete(0, tk.END)  # Clear the current file path entry
    file_path_entry.insert(tk.END, file_path)  # Insert the selected file path

# Create the browse button for selecting a file
browse_file_button = ttk.Button(export_frame, text="Browse", command=browse_file)
browse_file_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create the file path entry field
file_path_entry = ttk.Entry(export_frame, width=30)
file_path_entry.pack(side=tk.LEFT, padx=5, pady=5)

file_format_label = ttk.Label(export_frame, text="File Format:")
file_format_label.pack(side=tk.LEFT, padx=5, pady=5)
file_format_combobox = ttk.Combobox(export_frame, values=["png", "jpg", "pdf"], width=10)
file_format_combobox.pack(side=tk.LEFT, padx=5, pady=5)

# Function to handle graph export
def export_graph():
    file_path = file_path_entry.get()
    file_format = file_format_combobox.get()

    if file_path and file_format:
        canvas.figure.savefig(file_path, format=file_format)
        messagebox.showinfo("Export Success", "Graph exported successfully!")
    else:
        messagebox.showwarning("Export Error", "Please provide valid file path and format.")

# Add a button to trigger graph export
export_button = ttk.Button(options_frame, text="Export Graph", command=export_graph)
export_button.pack(side=tk.TOP, padx=5, pady=5)


# Start the Tkinter event loop
window.mainloop()
