import os
import pandas as pd
import plotly.express as px
from graphs.graphutils import colors, find_endpts
from .network import NodeNetwork

def generate_interaction_graph(directory):
    # Dynamically find the relevant CSV file (e.g., 'MKJH-popularities.csv')
    file_path = None
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('popularities.csv'):
                file_path = os.path.join(root, file)
                break

    if not file_path:
        raise FileNotFoundError("The expected 'popularities.csv' file was not found in the directory.")
    
    # Load the data
    popularity_data = pd.read_csv(file_path)

    # Initialize the node network
    player_names = popularity_data['agent'].unique().tolist()
    init_popularities = popularity_data.groupby('agent')['popularity'].mean().values

    network = NodeNetwork()
    network.setupPlayers(player_names)
    network.initNodes(init_popularities)

    # Now we can update the network and visualize it
    adj_matrix = pd.read_csv(os.path.join(directory, "interaction_matrix.csv")).values
    pops = popularity_data['popularity'].values
    network.update(adj_matrix, pops)

    # Create a plotly figure with nodes and edges based on `network`
    fig = px.scatter(x=[node.getCurrentPos()[0] for node in network.nodes[-1]],
                     y=[node.getCurrentPos()[1] for node in network.nodes[-1]],
                     size=[node.popularity for node in network.nodes[-1]],
                     hover_name=[node.name for node in network.nodes[-1]])

    # Optionally add edges/lines between nodes to represent relationships
    for node_i, node_j in zip(*adj_matrix.nonzero()):
        fig.add_shape(type="line",
                      x0=network.nodes[-1][node_i].getCurrentPos()[0],
                      y0=network.nodes[-1][node_i].getCurrentPos()[1],
                      x1=network.nodes[-1][node_j].getCurrentPos()[0],
                      y1=network.nodes[-1][node_j].getCurrentPos()[1],
                      line=dict(color="LightSeaGreen", width=2))

    return fig
