import odswriter
import data_to_excel
import numpy as np
import pandas as pd

# Read the raw data
game_data = pd.read_csv('utah_florida_raw.csv')

# Remove information that will not be used.
game_data = game_data.drop(columns=['Id','Offense Conference','Defense Conference','Home','Away','Game Id','Drive Id','Offense Timeouts','Defense Timeouts','Yard Line','Ppa','Wallclock'])

i=1
while i <= game_data.shape[0]:
    if 'Kickoff' in game_data.loc[i,'Play Type']:
        game_data=game_data.drop(index=i)
    elif 'Punt' in game_data.loc[i, 'Play Type']:
        game_data=game_data.drop(index=i)
    elif 'Field Goal' in game_data.loc[i, 'Play Type']:
        game_data=game_data.drop(index=i)
    i+=1

# Sort play data by team on offense.
primary_off = game_data.loc[game_data['Offense']=='Utah']
secondary_off = game_data.loc[game_data['Offense']=='Florida']

# row = [5,'UTH',1,'O']

# Experiment with excel files
df = pd.DataFrame([['=SUM(1,1)','=SUM(A2+1)'],['=SUM(1,1)','=A3-1']], columns=['Foo','Bar'])
with pd.ExcelWriter("experiment.xlsx") as writer:
    df.to_excel(writer)
