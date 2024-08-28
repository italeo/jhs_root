import os
import pandas as pd
from transformers import pipeline
import plotly.express as px

def generate_sentiment_graph(directory):
    # Dynamically find the relevant CSV file (e.g., 'MKJH-messages-dataset.csv')
    file_path = None
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('messages-dataset.csv'):
                file_path = os.path.join(root, file)
                break

    if not file_path:
        raise FileNotFoundError("The expected 'messages-dataset.csv' file was not found in the directory.")

    # Load the data
    data = pd.read_csv(file_path)

    if 'Message' in data.columns:
        # Initialize the sentiment analysis pipeline with a specific model
        sentiment_analysis = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

        # Apply sentiment analysis to the text data
        data['sentiment'] = data['Message'].apply(lambda x: sentiment_analysis(x)[0]['label'])

        # Group by player and sentiment, and count the number of messages
        sentiment_counts = data.groupby(['Name', 'sentiment']).size().unstack(fill_value=0)

        # Reset the index to use 'Name' as a column for Plotly
        sentiment_counts = sentiment_counts.reset_index()

        # Create a stacked bar chart using Plotly
        fig = px.bar(sentiment_counts, x='Name', y=['POSITIVE', 'NEGATIVE'],
                     title='Sentiment Analysis by Player',
                     labels={'value': 'Number of Messages', 'Name': 'Player'},
                     color_discrete_map={'POSITIVE': 'blue', 'NEGATIVE': 'red'})

        # Update layout to improve readability
        fig.update_layout(barmode='stack')

        return fig
    else:
        raise ValueError("The expected 'Message' column was not found in the data.")
