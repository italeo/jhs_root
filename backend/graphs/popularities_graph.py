import os
import pandas as pd
import plotly.express as px

def generate_popularity_graph(directory):
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

    # Drop the irrelevant column (Unnamed: 3) if it exists
    if 'Unnamed: 3' in popularity_data.columns:
        popularity_data = popularity_data.drop(columns=['Unnamed: 3'])

    # Create a line chart to visualize popularity scores across rounds
    fig = px.line(popularity_data, x='round', y='popularity', color='agent',
                  title='Popularity Scores Across Rounds',
                  labels={'round': 'Round Number', 'popularity': 'Popularity Score', 'agent': 'Player'})

    # Highlight the player with the highest score in the final round
    final_round = popularity_data[popularity_data['round'] == popularity_data['round'].max()]
    winner = final_round.loc[final_round['popularity'].idxmax()]

    fig.add_annotation(x=winner['round'], y=winner['popularity'],
                       text=f"Winner: {winner['agent']}",
                       showarrow=True, arrowhead=1)

    return fig
