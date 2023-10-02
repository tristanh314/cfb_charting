import numpy as np
import pandas as pd

# Read the raw data
game_data = pd.read_csv('utah_florida_raw.csv')

# Remove information that will not be used.
game_data = game_data.drop(columns=['Id','Offense Conference','Defense Conference','Home','Away','Game Id','Drive Id','Offense Timeouts','Defense Timeouts','Yard Line','Ppa','Wallclock'])

i=1
while i <= game_data.shape[0]:
    if "Kickoff" in game_data.loc[i,'Play Type']:
        game_data=game_data.drop(index=i)
    i+=1
    

# home_off = game_data.loc[game_data['Offense']=='Utah']
# home_def = game_data.loc[game_data['Defense']=='Utah']