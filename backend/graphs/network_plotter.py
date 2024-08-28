import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image, ImageOps

from network import NodeNetwork

"""color gang"""
player2color = {
    'Govt': '#e7298a',
    'CAT': '#fc8d62',
    'Gene': '#8da0cb',
    'Human': '#34bdc5'
}

def load_pop_data(game_code, folder):
    df = pd.read_csv(f'./study_games/{folder}/jhg_[\'{game_code}\'].csv')
    plrs = len([c for c in df.columns if c[:3] == 'pid'])
    pop_cols = [f'p{i}' for i in range(plrs)]
    pid_cols = [f'pid{i}' for i in range(plrs)]
    action_cols = [f'{i}-T-{j}' for i in range(plrs) for j in range(plrs)]
    infl_cols = [f'{i}-I-{j}' for i in range(plrs) for j in range(plrs)]
    pop_mat = df[pop_cols].to_numpy()
    pids = {i: t for i, t in enumerate(df[pid_cols].to_numpy()[0])}
    actions_mat = df[action_cols].to_numpy().reshape(-1, plrs, plrs)
    infl_mat = df[infl_cols].to_numpy().reshape(-1, plrs, plrs)
    params = {
        'alpha': df['alpha'][0],
        'beta': df['beta'][0],
        'give': df['give'][0],
        'keep': df['keep'][0],
        'steal': df['steal'][0],
        'num_players': plrs
    }

    return pids, pop_mat, actions_mat, infl_mat, params

def load_chat_data(game_code, folder):
    df = pd.read_csv(f'./study_games/{folder}/chat_{game_code}.csv')
    plrs = len([c for c in df.columns if c[:3] == 'pid'])
    #print("players:\n" + str(plrs))
    pop_cols = [f'p{i}' for i in range(plrs)]
    pid_cols = [f'pid{i}' for i in range(plrs)]
    action_cols = [f'{i}-M-{j}' for i in range(plrs) for j in range(plrs)]
    infl_cols = [f'{i}-I-{j}' for i in range(plrs) for j in range(plrs)]
    chat_mat = df[pop_cols].to_numpy()
    pids = {i: t for i, t in enumerate(df[pid_cols].to_numpy()[0])}
    chat_actions_mat = df[action_cols].to_numpy().reshape(-1, plrs, plrs)
    chat_infl_mat = df[infl_cols].to_numpy().reshape(-1, plrs, plrs)
    params = {
        'alpha': df['alpha'][0],
        'num_players': plrs
    }

    return pids, chat_mat, chat_actions_mat, chat_infl_mat, params

class NetworkPlot():
    def __init__(self, game_code, folder):
        self.game_code = game_code
        self.folder = folder

    def plot_network(self, rounds):
        print('gamecode: ' + self.game_code)
        pids, chat_mat, chat_actions_mat, chat_infl_mat, params = load_chat_data(self.game_code,self.folder)
        pids, pop_mat, actions_mat, infl_mat, params = load_pop_data(self.game_code, self.folder)
        #print(pop_mat.shape, actions_mat.shape, infl_mat.shape)
        #print(chat_mat.shape, chat_actions_mat.shape,chat_infl_mat.shape)

        dpi = 200
        if len(rounds) == 0:
            rounds = [i for i in range(pop_mat.shape[0])]
        fig = plt.figure(figsize=(2*len(rounds), 5), dpi=dpi)

        names = [f'p{k}' for k, v in pids.items()]
        player_types = {f'p{k}': v for k, v in pids.items()}
        #letters = 'ABCDEFGH'
        #name2codename = {n: letters[i] for i, n in enumerate(names)}
        name2codename = {}
        if len(set([v for k, v in pids.items()])) > 1:
            #name2color = {f'p{k}': '#34bdc5' if v == 'Human' else '#f47c6f' for k, v in pids.items()}
            name2color = {f'p{k}': player2color.get(v, '#f47c6f') for k, v in pids.items()}
            legend_colors = {v: player2color.get(v, '#f47c6f') for k, v in pids.items()}
        else:
            name2color = None
            legend_colors = None

        net = NodeNetwork()
        net.setupPlayers(names, player_types)
        net.initNodes(init_pops=pop_mat[0])

        chatNet = NodeNetwork()
        chatNet.setupPlayers(names, player_types)
        chatNet.initNodes(init_pops=chat_mat[0])

        gs = GridSpec(2, len(rounds), figure=fig)
        ids = [(0, i)for i in range(len(rounds))]

        for r in range(pop_mat.shape[0]):
            net.update(infl_mat[r], pop_mat[r])
            if r in rounds:
                round_idx = rounds.index(r)
                ax = fig.add_subplot(gs[ids[round_idx][0], ids[round_idx][1]], facecolor='c' if r%2 ==1 else 'm', ymargin=-.4)
                net.graphExchange(ax, fig, actions_mat[r], color_lookup=name2color, name_lookup=name2codename)
                ax.set_title(f'Token Round {r}', fontsize=12, loc='center', y=-0.09)

        for r in range(chat_mat.shape[0]):
            chatNet.update(chat_infl_mat[r], chat_mat[r])
            if r in rounds:
                round_idx = rounds.index(r)
                chatAx = fig.add_subplot(gs[1, ids[round_idx][1]], facecolor='c' if r%2 ==1 else 'm', ymargin=-.4)
                chatNet.graphExchange(chatAx, fig, chat_actions_mat[r], color_lookup=name2color, name_lookup=name2codename)
                chatAx.set_title(f'Chat Round {r}', fontsize=12, loc='center', y=-0.09)


            

        fig.subplots_adjust(wspace=0.0, hspace=0.00)

        #plt.show()
        image_path = f'./images/networkplots/networkplot_{self.game_code}.png'
        plt.savefig(image_path)

        image = Image.open(image_path)

        gray_image = ImageOps.grayscale(image)

        threshold_value = 254  # Adjust this value as needed
        thresholded_image = gray_image.point(lambda p: p < threshold_value and 255)

        bbox = thresholded_image.getbbox()

        cropped_image = image.crop(bbox)

        cropped_image.save(image_path)
        cropped_image.show()

