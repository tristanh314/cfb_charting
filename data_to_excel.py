import numpy as np
import pandas as pd
import odswriter as ods

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
    if 'Touchdown' in dataframe.loc[index]['Play Type']:
        return 't'
    elif 'Penalty' in dataframe.loc[index]['Play Type'] and dataframe[index]['Down'] == 1 and dataframe[index-1]['Down']:
        return 'x'
    else:
        return ''

abreviations = game_data['Play Type'].apply(abrev)
game_data['Play Abrev'] = abreviations
# Sort play data by team on offense.
primary_off = game_data.loc[game_data['Offense']=='Utah'].reset_index().drop(columns='index')
secondary_off = game_data.loc[game_data['Offense']=='Florida'].reset_index().drop(columns='index')

# Create a row of values to write to the ods file.
index=0
line=index+1
row_1=[
    5, #A
     'UTH',#B
     1,#C
     'O',#D
     primary_off.loc[0]['Down'],#E
     primary_off.loc[0]['Distance'],#F
     primary_off.loc[0]['Play Abrev'],#G
     f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
     1,#I
     1,#J
     is_td(primary_off,0),#K
     '',#L
     '',#M
     f'=IF(G{line}="?",CONCAT(AQ{line},"Q ",AR{line},":",TEXT(AS{line} ,"00")),"")',#N
     '',#O
     '',#P
     '',#Q
     '',#R
     '',#S
     '',#T
     '',#U
     '',#V
     '',#W
     '',#X
     '',#Y
     '',#Z
     '',#AA
     '',#AB
     '',#AC
     '',#AD
     '',#AE
     np.NaN,#AF
     '',#AG
     '',#AH
     '',#AI
     f'=IF(K{line}="t","o",IF(E{line+1}="1st","o","d"))',#AJ
     f'=IF((F{line}-F{line+1})<=1,"d",IF((F{line}-F{line+1})>F{line}/3,"o","d"))',#AK
     f'=IF((F{line}-F{line+1})<=1,"d",IF((F{line}-F{line+1})>=F{line}/2,"o","d"))',#AL
     '',#AM
     primary_off.loc[0]['Offense Score'],#AN
     primary_off.loc[0]['Defense Score'],#AO
    '',#AP
    primary_off.loc[0]['Period'],#AQ
    primary_off.loc[0]['Clock Minutes'],#AR
    primary_off.loc[0]['Clock Seconds'],#AS
    primary_off.loc[0]['Yards To Goal'],#AT
    '',#Au
    primary_off.loc[0]['Yards Gained'],#AV
    primary_off.loc[0]['Play Type'],#AW
    primary_off.loc[0]['Play Text'],#AX
    '',#AY
    '',#AZ
    '',#BA
    '',#BB
    '',#BC
    '',#BD
    f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
    f'=BE{line}=AV{line}',#BF
    ]
# Write row to an ods file.
with ods.writer(open('test_multi.ods','wb')) as file:
    primary_sheet = file.new_sheet('UTH Off, FLA Def')
    primary_sheet.writerow(row_1)