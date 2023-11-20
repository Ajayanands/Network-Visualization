import tkinter as tk
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_network_graph(nodes_data, edges_data):
    G = nx.Graph()
    G.add_nodes_from(nodes_data)
    G.add_weighted_edges_from(edges_data)
    return G


def display_network_graph(G, pos=None):
    if pos is None:
        pos = nx.spring_layout(G)  # Use spring layout as default

    # Clear the plot
    ax.clear()

      # Draw nodes
    node_colors = {
        'router': 'lightblue',
        'switch': 'lightgreen',
        'server': 'lightpink'
    }
    node_shapes = {
        'router': 's',   # Rectangles for routers
        'switch': 'o',   # Circles for switches
        'server': '^'    # Triangles for servers
    }

    for node, data in G.nodes(data=True):
        node_type = data.get('type', 'unknown')
        node_color = node_colors.get(node_type, 'gray')
        node_shape = node_shapes.get(node_type, 'o')  # Default shape is circle
        nx.draw_networkx_nodes(G, pos, nodelist=[node], ax=ax, node_shape=node_shape, node_color=node_color, node_size=800)


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


def display_shortest_path(G,source_node, target_node, ):
    shortest_path = nx.shortest_path(G, source=source_node, target=target_node, weight='weight')
    path_text = ' -> '.join(shortest_path)
    messagebox.showinfo("Shortest Path", f"The shortest path from {source_node} to {target_node} is:\n{path_text}")


def get_node_icon(node_type):
    if node_type == 'router':
        return ('s', 'Square')  # Square shape
    elif node_type == 'switch':
        return ('^', 'Circle')  # Triangle shape
    elif node_type == 'server':
        return ('o', 'Triangle')  # Circle shape
    else:
        return ('N/A', 'Unknown')  # Return 'N/A' for unknown types


def add_node():
    node_name = node_name_entry.get()
    node_type = node_type_combobox.get()
    node_info = node_info_entry.get()

    if node_name and node_type:
        G.add_node(node_name, type=node_type, info=node_info)
        nodes_data.append((node_name, {'type': node_type, 'info': node_info}))
        node_name_entry.delete(0, tk.END)
        node_info_entry.delete(0, tk.END)
        node_name_combobox['values'] = list(G.nodes())
        display_network_graph(G)
    else:
        messagebox.showwarning("Missing Information", "Please provide a node name and select a node type.")




def add_edge():
    node1 = node1_combobox.get()
    node2 = node2_combobox.get()
    weight = weight_entry.get()

    if node1 and node2 and weight:
        G.add_edge(node1, node2, weight=float(weight))
        edges_data.append((node1, node2, float(weight)))
        node1_combobox.set('')
        node2_combobox.set('')
        weight_entry.delete(0, tk.END)
        display_network_graph(G)
    else:
        messagebox.showwarning("Missing Information", "Please select two nodes and provide a weight.")


def display_node_info():
    node_name = node_name_combobox.get()
    if node_name:
        node_type = G.nodes[node_name].get('type', 'unknown')
        node_info = G.nodes[node_name].get('info', '')
        messagebox.showinfo(f"{node_name} Information", f"\n\nNode Info:\n\n{node_info}")


def export_graph():
    file_path = file_path_entry.get()
    file_format = file_format_combobox.get()

    if file_path and file_format:
        canvas.figure.savefig(file_path, format=file_format)
        messagebox.showinfo("Export Success", "Graph exported successfully!")
    else:
        messagebox.showwarning("Export Error", "Please provide a valid file path and format.")


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
figure = plt.figure(figsize=(6, 4))
ax = figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Initialize graph data
nodes_data = []  # List of node data (name, attributes)
edges_data = []  # List of edge data (node1, node2, weight)
G = create_network_graph(nodes_data, edges_data)

# Create and display the network graph
display_network_graph(G)

# Create a frame for adding nodes
add_node_frame = tk.Frame(options_frame)
add_node_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create a button for adding nodes
add_node_button = ttk.Button(add_node_frame, text="Add Node", command=add_node)
add_node_button.pack(side=tk.LEFT, padx=5, pady=5)



# Create input fields for node information
node_name_label = tk.Label(add_node_frame, text="Node Name:")
node_name_label.pack(side=tk.LEFT, padx=5, pady=5)
node_name_entry = tk.Entry(add_node_frame, width=15)
node_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

node_type_label = tk.Label(add_node_frame, text="Node Type:")
node_type_label.pack(side=tk.LEFT, padx=5, pady=5)
node_type_combobox = ttk.Combobox(add_node_frame, values=['router', 'switch', 'server'], width=10)
node_type_combobox.pack(side=tk.LEFT, padx=5, pady=5)

node_info_label = tk.Label(add_node_frame, text="Node Info:")
node_info_label.pack(side=tk.LEFT, padx=5, pady=5)
node_info_entry = tk.Entry(add_node_frame, width=15)
node_info_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button to add the node
add_node_button = ttk.Button(add_node_frame, text="Add Node", command=add_node)
add_node_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame for adding edges
add_edge_frame = tk.Frame(options_frame)
add_edge_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create comboboxes and entry field for adding edges
node1_label = tk.Label(add_edge_frame, text="Node 1:")
node1_label.pack(side=tk.LEFT, padx=5, pady=5)
node1_combobox = ttk.Combobox(add_edge_frame, values=list(G.nodes()), width=10)
node1_combobox.pack(side=tk.LEFT, padx=5, pady=5)

node2_label = tk.Label(add_edge_frame, text="Node 2:")
node2_label.pack(side=tk.LEFT, padx=5, pady=5)
node2_combobox = ttk.Combobox(add_edge_frame, values=list(G.nodes()), width=10)
node2_combobox.pack(side=tk.LEFT, padx=5, pady=5)

weight_label = tk.Label(add_edge_frame, text="Weight:")
weight_label.pack(side=tk.LEFT, padx=5, pady=5)
weight_entry = tk.Entry(add_edge_frame, width=10)
weight_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button to add the edge
add_edge_button = ttk.Button(add_edge_frame, text="Add Edge", command=add_edge)
add_edge_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame to hold the comboboxes for node selection
combobox_frame = tk.Frame(options_frame)
combobox_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create the comboboxes for source and target nodes
source_label = ttk.Label(combobox_frame, text="Source Node:")
source_label.pack(side=tk.LEFT, padx=5, pady=5)
source_combobox = ttk.Combobox(combobox_frame, values=list(G.nodes()), width=15)
source_combobox.pack(side=tk.LEFT, padx=5, pady=5)

target_label = ttk.Label(combobox_frame, text="Target Node:")
target_label.pack(side=tk.LEFT, padx=5, pady=5)
target_combobox = ttk.Combobox(combobox_frame, values=list(G.nodes()), width=15)
target_combobox.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button to find the shortest path
shortest_path_button = ttk.Button(
    combobox_frame,
    text="Find Shortest Path",
    command=lambda: display_shortest_path(G, source_combobox.get(), target_combobox.get())
)
shortest_path_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame for displaying node information
node_info_frame = tk.Frame(options_frame)
node_info_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create a combobox for selecting a node to display information
node_name_combobox = ttk.Combobox(node_info_frame, values=list(G.nodes()), width=15)
node_name_combobox.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button to display node information
display_node_info_button = ttk.Button(node_info_frame, text="Display Node Info", command=display_node_info)
display_node_info_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame for export options
export_frame = tk.Frame(options_frame)
export_frame.pack(side=tk.TOP, padx=5, pady=5)

# Function to open the file explorer and select a file path
def browse_file():
    file_path = askdirectory()
    file_path_entry.delete(0, tk.END)  # Clear the current file path entry
    file_path_entry.insert(tk.END, file_path)  # Insert the selected file path

# Create a button to open the file explorer and select a file path
browse_button = ttk.Button(export_frame, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create an entry field to display the selected file path
file_path_entry = ttk.Entry(export_frame, width=30)
file_path_entry.pack(side=tk.LEFT, padx=5, pady=5)

file_format_label = ttk.Label(export_frame, text="File Format:")
file_format_label.pack(side=tk.LEFT, padx=5, pady=5)
file_format_combobox = ttk.Combobox(export_frame, values=["png", "jpg", "pdf"], width=8)
file_format_combobox.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button to export the graph
export_button = ttk.Button(export_frame, text="Export Graph", command=export_graph)
export_button.pack(side=tk.LEFT, padx=5, pady=5)

# Start the main event loop
window.mainloop()
