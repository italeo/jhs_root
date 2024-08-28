"""
make sure to uncomment everything that is commented to get the original CSV format

find a way to map data based on chat activity; perhaps loop through each chat and 
add to a counter for each player's name

"""

import pandas as pd
import json
import os

#print(os.getcwd()) = /home/broeli/Documents/Practice_Game

jfName = 'CHLN'
load_path = f'./study_games/jsons/{jfName}.json'
save_path = './study_games/csvs'

print(f'Processing {load_path}')

with open(load_path) as json_file:

    #access full json file:
    data_dict = json.load(json_file)
    #type(data_dict) = <class 'dict'>

    # gets prefix of file (in tis case 'jhg_VKFD')
    file_prefix = jfName.rsplit('.', 1)

    print(file_prefix)
    #['jhg_VKFD', 'json']

    #access game parameters:
    alpha = data_dict["gameParams"]["popularityFunctionParams"]["alpha"]
    beta = data_dict["gameParams"]["popularityFunctionParams"]["beta"]
    c_g = data_dict["gameParams"]["popularityFunctionParams"]["cGive"]
    c_k = data_dict["gameParams"]["popularityFunctionParams"]["cKeep"]
    c_s = data_dict["gameParams"]["popularityFunctionParams"]["cSteal"]
    num_rounds = len(data_dict['popularities'])

    #(alpha) = 0.2
    #(beta) = 0.5
    #(c_g) = 1.3
    #(c_k) = 0.95
    #(c_s) = 1.6
    #(num_rounds) = 13


    game_dict = {
        c: [] for c in 'round,alpha,beta,give,keep,steal'.split(',')
        #c: [] for c in 'round'.split(',')
    }

    players2code = {}


    plrs = list(data_dict["popularities"]["round_1"].keys())
    #['Abinadi', 'Alma', 'Brother of Jared', 'Helaman', 'King Lamoni', 'King Noah', 'Lemuel', 'Teancum']

    #this section adds column names
    game_dict = {**game_dict, **{f'p{i}': [] for i in range(len(plrs))}}
    game_dict = {**game_dict, **{f'{i}-T-{j}': [] for i in range(len(plrs)) for j in range(len(plrs))}}
    game_dict = {**game_dict, **{f'{i}-I-{j}': [] for i in range(len(plrs)) for j in range(len(plrs))}}
    game_dict = {**game_dict, **{f'pid{i}': [] for i in range(len(plrs))}}
    for i, player in enumerate(plrs):
        players2code[player] = i

    #this section populates rows under columns
    for r in range(num_rounds):
        game_dict['round'].append(r)
        game_dict['alpha'].append(alpha)
        game_dict['beta'].append(beta)
        game_dict['give'].append(c_g)
        game_dict['keep'].append(c_k)
        game_dict['steal'].append(c_s)

        round_key = f'round_{r+1}'
        action_round_key = f'round_{r}'
        for n, p in data_dict['popularities'][round_key].items():
            game_dict[f'p{players2code[n]}'].append(p)
            game_dict[f'pid{players2code[n]}'].append('Human')

        
        for receiver, infl_dict in data_dict['influences'][round_key].items():
            receiver_id = players2code.get(receiver, None)
            for giver, val in infl_dict.items():
                if giver == '__intrinsic__':
                    continue
                giver_id = players2code.get(giver, None)
                if receiver_id is not None:
                    game_dict[f'{giver_id}-I-{receiver_id}'].append(val)

        if r != 0:
            for giver, action_dict in data_dict['transactions'][action_round_key].items():
                giver_id = players2code.get(giver, None)
                for receiver, val in action_dict.items():
                    receiver_id = players2code.get(receiver, None)
                    if receiver_id is not None:
                        game_dict[f'{giver_id}-T-{receiver_id}'].append(val)
        else:
            # dumb hack to handle 0 mat for round 1
            for receiver, infl_dict in data_dict['influences'][round_key].items():
                receiver_id = players2code.get(receiver, None)
                for giver, val in infl_dict.items():
                    if giver == '__intrinsic__':
                        continue
                    giver_id = players2code.get(giver, None)
                    if receiver_id is not None:
                        game_dict[f'{giver_id}-T-{receiver_id}'].append(0)

        expeted_len = len(game_dict['round'])
        for k, v in game_dict.items():
            if len(v) != expeted_len:
                parts = k.split('-')
                if parts[0] != parts[-1]:
                    game_dict[k].append(0)
                else:
                    game_dict[k].append(2 * len(plrs))
                print(f'Filling in {k} for {round_key} as {game_dict[k][-1]}')

    game_df = pd.DataFrame.from_dict(game_dict)
    game_df.to_csv(f'{save_path}/jhg_{file_prefix}.csv', index=False)

