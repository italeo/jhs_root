import numpy as np
import pandas as pd

df = pd.read_csv("MKJH-popularities.csv")

numRounds = len(df['round'].unique()) 
numPlayers = len(df['agent'].unique()) 
agentNames = df['agent'].unique()

pop_raw = df['popularity'].to_numpy()

pop_array = pop_raw.reshape(numRounds, numPlayers)


newdf = pd.DataFrame(
    {'round' : np.arange(numRounds),
     **{agentNames[i] : pop_array[:,i]
        for i in range(numPlayers)         
     }}
)


game_df = pd.DataFrame.from_dict(newdf)
game_df.to_csv(f'newConversion.csv', index=False)
