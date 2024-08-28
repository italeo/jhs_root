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

class MessageData:
    def __init__(self, sender, message):
        self.sender = sender
        #self.receiver = receiver
        self.message = message
    
    def show(self):
        print("Sender: " + self.sender + "\nMessage: " + self.message)
        #"\nReceiver: " + self.receiver +


#function to calculate total number of chats in the game
def calculate_num_chats(json_data):
    num_chats = 0
    for conversation in json_data:
        messages = conversation['messages']
        for msg_id, message in messages.items():
        # Extract round information
            if message['from'] != 'Game':
                num_chats += 1
    #print(num_chats)
    return num_chats

def prod_msg_data_dict(json_data):
    data_dict = {}

    for conversation in json_data['chatInfo'].values():
        messages = conversation['messages']
        current_round = 1

        # Find the starting round number if present
        for message in messages.values():
            if message['runtimeType'] == 'gameNotification' and message['body'].startswith("Round"):
                current_round = int(message['body'].split(" ")[1]) - 1
                break

        for msg_id, message in messages.items():
            # Extract round information
            if message['from'] == 'Game' and message['body'].startswith("Round"):
                current_round = int(message['body'].split(" ")[1])
                if current_round not in data_dict:
                    data_dict[current_round] = {}
            else:
                sender = message['from']
                body = message['body']
                msg = MessageData(sender, body)
                data_dict.setdefault(current_round, {})[msg_id] = msg

    #print(data_dict)
    game_df = pd.DataFrame.from_dict(data_dict)
    game_df.to_csv('study_games/test_csvs/data_dict.csv', index=False)
    return data_dict


# Function to process the JSON data
def process_json_to_csv(json_data, output_dir, file_name):

    data_dict = prod_msg_data_dict(json_data)

    # Dictionary to hold the count of messages per player per round
    all_data = defaultdict(lambda: defaultdict(int))

    num_rounds = len(json_data['popularities'])
    num_chats = calculate_num_chats(json_data['chatInfo'].values())



    all_data = {**all_data, **{'message_num' : list(range(0, num_chats+1))}}

    #list of name values
    plrs = list(json_data["popularities"]["round_1"].keys())

    #map of enumerators
    players2code = {}
    for i, player in enumerate(plrs):
        players2code[player] = i
    
    all_data = {**all_data, **{f'round': [0]*(num_chats+1)}}
    all_data = {**all_data, **{f'sender': ['']*(num_chats+1)}}
    all_data = {**all_data, **{f'message': ['']*(num_chats+1)}}

    #print(all_data)
    
    #keep track of which message is being sent; adjust per
    msg_num = 1
    for round_number, messages in data_dict.items():
        #print(f"Round: {round_number}")
    
        # Loop through each message in the current round
        for msg_id, message_data in messages.items():
            #print(f"  Message ID: {msg_id}")
            #message_data.show()
            all_data["round"][msg_num] = round_number
            all_data["sender"][msg_num] = message_data.sender
            all_data["message"][msg_num] = message_data.message
            #print('message number:', msg_num, '\n')
            msg_num += 1

    #print(all_data)
    game_df = pd.DataFrame.from_dict(all_data)
    game_df.to_csv(f'{output_dir}/{file_name}.csv', index=False)


file_name = "PXWT"

# Read the JSON data from a file
with open(f'./study_games/jsons/{file_name}.json', 'r') as file:
    json_data = json.load(file)

# Define the directory where you want to save the CSV file
output_directory = './study_games/csvs'  # Change this to your desired directory

# Process the JSON data and create the CSV file
process_json_to_csv(json_data, output_directory, file_name)
