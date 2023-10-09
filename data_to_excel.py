import numpy as np
import pandas as pd

# Read the raw data
game_data = pd.read_csv('utah_florida_raw.csv')

# Remove information that will not be used.
game_data = game_data.drop(columns=['Id','Offense Conference','Defense Conference','Home','Away','Game Id','Drive Id','Offense Timeouts','Defense Timeouts','Yard Line','Ppa','Wallclock'])

i=0
while i <= game_data.shape[0]:
    if 'Kickoff' in game_data.loc[i]['Play Type']:
        game_data=game_data.drop(index=i)
    elif 'Punt' in game_data.loc[i]['Play Type']:
        game_data=game_data.drop(index=i)
    elif 'Field Goal' in game_data.loc[i]['Play Type']:
        game_data=game_data.drop(index=i)
    elif 'Timeout' in game_data.loc[i]['Play Type']:
        game_data=game_data.drop(index=i)
    elif 'End' in game_data.loc[i]['Play Type']:
        game_data=game_data.drop(index=i)
    i+=1

# Functions to format information not in the raw stats
# Make play abreviations
def abrev(string):
    if 'Pass' in string:
        return 'p'
    elif 'Rush' in string:
        return 'r'
    else:
        return '?'

# Check for touchdowns or penalties
def is_td(dataframe, index):
    if 'Touchdown' in dataframe[index]['Play Type']:
        return 't'
    elif 'Penalty' in dataframe[index]['Play Type'] and dataframe[index]['Down'] == 1 and dataframe[index-1]['Down']:
        return 'x'
    else:
        return ''

abreviations = game_data['Play Type'].apply(abrev)
game_data['Play Abrev'] = abreviations
# Sort play data by team on offense.
primary_off = game_data.loc[game_data['Offense']=='Utah'].reset_index().drop(columns='index')
secondary_off = game_data.loc[game_data['Offense']=='Florida'].reset_index().drop(columns='index')

# Not ready for prime time
primary_array=np.array([
    [5, #A
     'UTH',#B
     1,#C
     'O',#D
     primary_off.loc[0]['Down'],#E
     primary_off.loc[0]['Distance'],#F
     primary_off[0]['Play Abrev'],#G
     '',#H
     1,#I
     1,#J
     is_td(primary_off,0),#
     ]
    ])
# for i in [1,primary_off.size[0]]:
#     row = [5,'UTH',i,'O']