import os
import re
import networkx as nx
import pandas as pd
import plotly.graph_objs as go
import community.community_louvain as community_louvain
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

def create_cluster_chat_graph(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Function to extract recipient from message
    def extract_recipient(message):
        match = re.search(r'@(\w+)', message)
        if match:
            return match.group(1)
        return None

    # Extract recipients
    df['Recipient'] = df['Message'].apply(extract_recipient)

    # Remove messages without a recipient
    df_filtered = df.dropna(subset=['Recipient'])

    # Create a directed graph
    G = nx.DiGraph()

    # Colors for nodes
    color_map = plt.get_cmap('tab20')
    colors = [mcolors.rgb2hex(color_map(i)[:3]) for i in range(color_map.N)]

    # Use a fixed position layout for consistency
    pos = nx.spring_layout(G)

    # Add edges and nodes to the graph with dynamic layout updates
    frames = []
    for i, (index, row) in enumerate(df_filtered.iterrows()):
        sender = row['Name'].strip().title()
        recipient = row['Recipient'].strip().title()

        if G.has_edge(sender, recipient):
            G[sender][recipient]['weight'] += 1
        else:
            G.add_edge(sender, recipient, weight=1)

        # Detect communities using the Louvain method
        partition = community_louvain.best_partition(G.to_undirected())

        # Assign a unique color to each community
        community_colors = {community: colors[i % len(colors)] for i, community in enumerate(set(partition.values()))}

        # Initialize new edge trace with proper list attributes
        edge_x, edge_y = [], []
        for edge in G.edges(data=True):
            x0, y0 = pos.get(edge[0], (0, 0))  # Default to (0,0) if no position is found
            x1, y1 = pos.get(edge[1], (0, 0))
            print(f"Appending to edge_x: {x0}, {x1}")  # Debugging line
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        # Initialize new node trace with proper list attributes
        node_x, node_y, node_text, node_size, node_color = [], [], [], [], []
        for node in G.nodes():
            x, y = pos.get(node, (0, 0))  # Default to (0,0) if no position is found
            print(f"Appending to node_x: {x}")  # Debugging line
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)  # Append text correctly
            node_size.append(10 + 2 * G.degree(node))
            node_color.append(community_colors.get(partition[node], '#000000'))

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            text=node_text,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                size=node_size,
                color=node_color,
                line=dict(width=2)
            )
        )

        # Add frame
        frames.append(go.Frame(data=[edge_trace, node_trace], name=str(i)))

    # Initial data
    fig = go.Figure(data=frames[0].data)

    # Add frames to the figure
    fig.frames = frames

    # Layout for animation
    fig.update_layout(
        title='<br>Cluster graph showing player mentions',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        updatemenus=[dict(type="buttons", showactive=True,
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None, dict(frame=dict(duration=500, redraw=True),
                                                         fromcurrent=True)])])]
    )

    return fig
