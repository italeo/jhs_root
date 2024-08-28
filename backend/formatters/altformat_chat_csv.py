'''
influences working, but need to standardize

'''


import json
import csv
import re
import numpy as np
import pandas as pd
import os
from collections import defaultdict

def extract_numbers_from_string(s,type):
    # Define the pattern to match the format "i-I-j"
    pattern = re.compile(r"^(\d+)-" + type + r"-(\d+)$")
    
    match = pattern.match(s)
    if match:
        i = match.group(1)
        j = match.group(2)
        return i, j
    else:
        # Handle other formats or skip them
        return None, None
    
def calculate_chat_influence(alpha,i,j,round,all_data):
    curMCol = f"{i}-M-{j}"
    curICol = f"{i}-I-{j}"
    x_val = all_data[curMCol][round]
    last_influence = all_data[curICol][round-1]
    influence = (alpha * x_val) + (1-alpha)*(last_influence)
    all_data[curICol][round] = influence

# Function to process the JSON data and count messages per player per round
def process_json_to_csv(json_data, output_dir, file_name):

    # Dictionary to hold the count of messages per player per round
    all_data = defaultdict(lambda: defaultdict(int))
    chat_counts = defaultdict(lambda: defaultdict(int))

    num_rounds = len(json_data['popularities'])
    num_players = len(json_data['players'])
    alpha = json_data["gameParams"]["popularityFunctionParams"]["alpha"]

    all_data = {**all_data, **{'round' : list(range(0, num_rounds+1))}}
    all_data = {**all_data, **{'alpha' : [alpha]*(num_rounds+1)}}

    #list of name values
    plrs = list(json_data["popularities"]["round_1"].keys())

    #map of enumerators
    players2code = {}
    for i, player in enumerate(plrs):
        players2code[player] = i

    all_data = {**all_data, **{f'p{i}': [0]*(num_rounds+1) for i in range(len(plrs))}}
    all_data = {**all_data, **{f'{i}-M-{j}': [0]*(num_rounds+1) for i in range(len(plrs)) for j in range(len(plrs))}}
    chat_counts = {**chat_counts, **{f'{i}-M-{j}': [0]*(num_rounds+1) for i in range(len(plrs)) for j in range(len(plrs))}}
    all_data = {**all_data, **{f'{i}-I-{j}': [0]*(num_rounds+1) for i in range(len(plrs)) for j in range(len(plrs))}}
    all_data = {**all_data, **{f'pid{i}': ["Human"]*(num_rounds+1) for i in range(len(plrs))}}

    for conversation in json_data['chatInfo'].values():
        messages = conversation['messages']
        if "participants" in conversation:
            participants = list(conversation['participants'])
        
        #find round starting number for particular chat
        for msg_id, message in messages.items():
            #if message['runtimeType'] == 'gameNotification' and message['body'].startswith("Round"):
            if message['body'].startswith("Round "):
                initial_round = int(message['body'].split(" ")[1]) - 1
                break
        
        current_round = initial_round

        for msg_id, message in messages.items():
            # Extract round information
            #if message['runtimeType'] == 'gameNotification' and message['body'].startswith("Round"):
            if message['body'].startswith("Round "): 
                current_round = int(message['body'].split(" ")[1])
            
            # Count messages for each player per round
            #elif message['runtimeType'] == 'identified':
            else: 
                #go through and get a round number here:
                ####################
                from_player = players2code[message['from']]
                
                receiving_players = [players2code[participants[i]] for i in range(len(participants)) if players2code[participants[i]] != from_player]
                
                #case global chat where participants is emptyi != None 
                if len(receiving_players) == 0:
                    receiving_players = [i for i in range(num_players) if i != from_player]
                
                for j in receiving_players:      
                    all_data[f"{from_player}-M-{j}"][current_round-1] += 1/len(receiving_players)
                    chat_counts[f"{from_player}-M-{j}"][current_round] += 1/len(receiving_players)

    #add functionality for using calculate influence matrix
    for column in all_data:
        i,j = extract_numbers_from_string(column, "M")
        if ((i != None) & (j != None)):
            for round in range(1, num_rounds + 1):
                calculate_chat_influence(alpha=alpha,i=i,j=j,round=round,all_data=all_data)

    #calculate total chat/round for each round for each player
    for column in chat_counts:
        i,j = extract_numbers_from_string(column, "M")
        for round in range(1, num_rounds + 1):
            all_data[f'p{i}'][round] += np.round(chat_counts[column][round], decimals=3)
    
    game_df = pd.DataFrame.from_dict(all_data)
    game_df.to_csv(f'{output_dir}/{file_name}.csv', index=False)

###########################

file_name = "PXWT"

# Read the JSON data from a file
with open(f'./study_games/jsons/{file_name}.json', 'r') as file:
    json_data = json.load(file)

# Define the directory where you want to save the CSV file
output_directory = './study_games/csvs'  # Change this to your desired directory

# Process the JSON data and create the CSV file
process_json_to_csv(json_data, output_directory, file_name)
