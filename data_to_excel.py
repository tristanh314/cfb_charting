import numpy as np
import pandas as pd
import odswriter as ods

############# USER INPUT REQUIRED #############
# INPUT RELATIVE PATH TO RAW DATA
game_data = pd.read_csv('cal_ors_raw.csv')
# INPUT RELATIVE PATH TO DESTINATION FILE
file_name = "CAL_ORS_TH.ods"
# SPECIFY NAMES AND ABBREVIATIONS TO USE.
game_num = 5
prime_team = "California"
sec_team = "Oregon State"
prime_abrev = "CAL"
sec_abrev  = "ORS"
######### DID YOU CHECK YOUR CHOICES? #########

# Remove information that will not be used.
game_data = game_data.drop(columns=['Id','Offense Conference','Defense Conference','Home','Away','Game Id','Drive Id','Offense Timeouts','Defense Timeouts','Yard Line','Ppa','Wallclock'])

i=0
while i < game_data.shape[0]:
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
    elif 'Penalty' in dataframe.loc[index]['Play Type'] and dataframe.loc[index]['Down'] == 1 and dataframe.loc[index-1]['Down'] == 1:
        return 'x'
    else:
        return ''
# Create appropriate play abbreviations
abreviations = game_data['Play Type'].apply(abrev)
game_data['Play Abrev'] = abreviations
# Format strings for down number.
def down_string(down):
    if down == 1:
        return '1st'
    elif down == 2:
        return '2nd'
    elif down == 3:
        return '3rd'
    elif down == 4:
        return '4th'
    else:
        return '?'

# Sort play data by team on offense.
primary_off = game_data.loc[game_data['Offense']==prime_team].reset_index().drop(columns='index')
secondary_off = game_data.loc[game_data['Offense']==sec_team].reset_index().drop(columns='index')

# Write rows of data for primary offesne to worksheet in the ODS file.
with ods.writer(open(file_name,'wb')) as file:
    # Write the sheet for the primary team's offense.
    sheet = file.new_sheet(f'{prime_abrev} Off, {sec_abrev} Def')
    index=0
    line=index+1
    while index < primary_off.shape[0]:
        if index > 0 and index < primary_off.shape[0] and int(primary_off.loc[index-1]['Drive Number']) != (int(primary_off.loc[index]['Drive Number'])):
            row = [
                game_num, #A
                prime_abrev,#B
                f'=IF(A{line-1}=A{line},C{line-1}+1,1)',#C
                'O',#D
                '',#E
                '',#F
                '',#G
                f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
                f'=IF(C{line}=1,1,IF(E{line}="","",IF(I{line-1}="",I{line-2}+1,I{line-1})))',#I
                f'=IF(E{line}="","",IF(E{line-1}="",1,1+J{line-1}))',#J
                '',#K
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
                '',#AN
                '',#AO
                '',#AP
                '',#AQ
                '',#AR
                '',#AS
                '',#AT
                '',#Au
                '',#AV
                '',#AW
                '',#AX
                '',#AY
                '',#AZ
                '',#BA
                '',#BB
                '',#BC
                '',#BD
                f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
                f'=BE{line}=AV{line}',#BF
                ]
            sheet.writerow(row)
            line+=1
        else:
            pass
        if line == 1:
            row=[
                game_num, #A
                prime_abrev,#B
                1,#C
                'O',#D
                down_string(primary_off.loc[index]['Down']),#E
                int(primary_off.loc[index]['Distance']),#F
                primary_off.loc[index]['Play Abrev'],#G
                f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
                '1',#I
                '1',#J
                is_td(primary_off,index),#K
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
                int(primary_off.loc[index]['Offense Score']),#AN
                int(primary_off.loc[index]['Defense Score']),#AO
                '',#AP
                int(primary_off.loc[index]['Period']),#AQ
                int(primary_off.loc[index]['Clock Minutes']),#AR
                int(primary_off.loc[index]['Clock Seconds']),#AS
                int(primary_off.loc[index]['Yards To Goal']),#AT
                '',#AU
                int(primary_off.loc[index]['Yards Gained']),#AV
                primary_off.loc[index]['Play Type'],#AW
                primary_off.loc[index]['Play Text'],#AX
                '',#AY
                '',#AZ
                '',#BA
                '',#BB
                '',#BC
                '',#BD
                f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
                f'=BE{line}=AV{line}',#BF
                ]
        elif line == 2:
                row=[
                game_num, #A
                prime_abrev,#B
                f'=IF(A{line-1}=A{line},C{line-1}+1,1)',#C
                'O',#D
                down_string(primary_off.loc[index]['Down']),#E
                int(primary_off.loc[index]['Distance']),#F
                primary_off.loc[index]['Play Abrev'],#G
                f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
                '1',#I
                f'=IF(E{line}="","",IF(E{line-1}="",1,1+J{line-1}))',#J
                is_td(primary_off,index),#K
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
                int(primary_off.loc[index]['Offense Score']),#AN
                int(primary_off.loc[index]['Defense Score']),#AO
                '',#AP
                int(primary_off.loc[index]['Period']),#AQ
                int(primary_off.loc[index]['Clock Minutes']),#AR
                int(primary_off.loc[index]['Clock Seconds']),#AS
                int(primary_off.loc[index]['Yards To Goal']),#AT
                '',#Au
                int(primary_off.loc[index]['Yards Gained']),#AV
                primary_off.loc[index]['Play Type'],#AW
                primary_off.loc[index]['Play Text'],#AX
                '',#AY
                '',#AZ
                '',#BA
                '',#BB
                '',#BC
                '',#BD
                f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
                f'=BE{line}=AV{line}',#BF
                ]
        else:
            row=[
                game_num, #A
                prime_abrev,#B
                f'=IF(A{line-1}=A{line},C{line-1}+1,1)',#C
                'O',#D
                down_string(primary_off.loc[index]['Down']),#E
                int(primary_off.loc[index]['Distance']),#F
                primary_off.loc[index]['Play Abrev'],#G
                f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
                f'=IF(C{line}=1,1,IF(E{line}="","",IF(I{line-1}="",I{line-2}+1,I{line-1})))',#I
                f'=IF(E{line}="","",IF(E{line-1}="",1,1+J{line-1}))',#J
                is_td(primary_off,index),#K
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
                int(primary_off.loc[index]['Offense Score']),#AN
                int(primary_off.loc[index]['Defense Score']),#AO
                '',#AP
                int(primary_off.loc[index]['Period']),#AQ
                int(primary_off.loc[index]['Clock Minutes']),#AR
                int(primary_off.loc[index]['Clock Seconds']),#AS
                int(primary_off.loc[index]['Yards To Goal']),#AT
                '',#AU
                int(primary_off.loc[index]['Yards Gained']),#AV
                primary_off.loc[index]['Play Type'],#AW
                primary_off.loc[index]['Play Text'],#AX
                '',#AY
                '',#AZ
                '',#BA
                '',#BB
                '',#BC
                '',#BD
                f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
                f'=BE{line}=AV{line}',#BF
                ]
        sheet.writerow(row)
        index+=1
        line+=1
    # Write the sheet for the secondary team's offense.
    sheet = file.new_sheet(f'{sec_abrev} Off, {prime_abrev} Def')
    index=0
    line=index+1
    while index < secondary_off.shape[0]:
        if index > 0 and index < secondary_off.shape[0] and int(secondary_off.loc[index-1]['Drive Number']) != (int(secondary_off.loc[index]['Drive Number'])):
            row = [
                game_num, #A
                sec_abrev,#B
                f'=IF(A{line-1}=A{line},C{line-1}+1,1)',#C
                'ddd',#D
                '',#E
                '',#F
                '',#G
                f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
                f'=IF(C{line}=1,1,IF(E{line}="","",IF(I{line-1}="",I{line-2}+1,I{line-1})))',#I
                f'=IF(E{line}="","",IF(E{line-1}="",1,1+J{line-1}))',#J
                '',#K
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
                '',#AN
                '',#AO
                '',#AP
                '',#AQ
                '',#AR
                '',#AS
                '',#AT
                '',#AU
                '',#AV
                '',#AW
                '',#AX
                '',#AY
                '',#AZ
                '',#BA
                '',#BB
                '',#BC
                '',#BD
                f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
                f'=BE{line}=AV{line}',#BF
                ]
            sheet.writerow(row)
            line+=1
        else:
            pass
        if line == 1:
            row=[
                game_num, #A
                sec_abrev,#B
                1,#C
                'ddd',#D
                down_string(secondary_off.loc[index]['Down']),#E
                int(secondary_off.loc[index]['Distance']),#F
                secondary_off.loc[index]['Play Abrev'],#G
                f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
                '1',#I
                '1',#J
                is_td(secondary_off,index),#K
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
                int(secondary_off.loc[index]['Offense Score']),#AN
                int(secondary_off.loc[index]['Defense Score']),#AO
                '',#AP
                int(secondary_off.loc[index]['Period']),#AQ
                int(secondary_off.loc[index]['Clock Minutes']),#AR
                int(secondary_off.loc[index]['Clock Seconds']),#AS
                int(secondary_off.loc[index]['Yards To Goal']),#AT
                '',#AU
                int(secondary_off.loc[index]['Yards Gained']),#AV
                secondary_off.loc[index]['Play Type'],#AW
                secondary_off.loc[index]['Play Text'],#AX
                '',#AY
                '',#AZ
                '',#BA
                '',#BB
                '',#BC
                '',#BD
                f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
                f'=BE{line}=AV{line}',#BF
                ]
        elif line == 2:
                row=[
                game_num, #A
                sec_abrev,#B
                f'=IF(A{line-1}=A{line},C{line-1}+1,1)',#C
                'ddd',#D
                down_string(secondary_off.loc[index]['Down']),#E
                int(secondary_off.loc[index]['Distance']),#F
                secondary_off.loc[index]['Play Abrev'],#G
                f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
                '1',#I
                f'=IF(E{line}="","",IF(E{line-1}="",1,1+J{line-1}))',#J
                is_td(secondary_off,index),#K
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
                int(secondary_off.loc[index]['Offense Score']),#AN
                int(secondary_off.loc[index]['Defense Score']),#AO
                '',#AP
                int(secondary_off.loc[index]['Period']),#AQ
                int(secondary_off.loc[index]['Clock Minutes']),#AR
                int(secondary_off.loc[index]['Clock Seconds']),#AS
                int(secondary_off.loc[index]['Yards To Goal']),#AT
                '',#AU
                int(secondary_off.loc[index]['Yards Gained']),#AV
                secondary_off.loc[index]['Play Type'],#AW
                secondary_off.loc[index]['Play Text'],#AX
                '',#AY
                '',#AZ
                '',#BA
                '',#BB
                '',#BC
                '',#BD
                f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
                f'=BE{line}=AV{line}',#BF
                ]
        else:
            row=[
                game_num, #A
                sec_abrev,#B
                f'=IF(A{line-1}=A{line},C{line-1}+1,1)',#C
                'ddd',#D
                down_string(secondary_off.loc[index]['Down']),#E
                int(secondary_off.loc[index]['Distance']),#F
                secondary_off.loc[index]['Play Abrev'],#G
                f'=IF(E{line}="","",IF(K{line}="x","d",IF(K{line}="p","d",IF(AJ{line}="o","o",IF(E{line}="1st",AK{line},IF(E{line}="2nd",AL{line},AJ{line}))))))',#H
                f'=IF(C{line}=1,1,IF(E{line}="","",IF(I{line-1}="",I{line-2}+1,I{line-1})))',#I
                f'=IF(E{line}="","",IF(E{line-1}="",1,1+J{line-1}))',#J
                is_td(secondary_off,index),#K
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
                int(secondary_off.loc[index]['Offense Score']),#AN
                int(secondary_off.loc[index]['Defense Score']),#AO
                '',#AP
                int(secondary_off.loc[index]['Period']),#AQ
                int(secondary_off.loc[index]['Clock Minutes']),#AR
                int(secondary_off.loc[index]['Clock Seconds']),#AS
                int(secondary_off.loc[index]['Yards To Goal']),#AT
                '',#AU
                int(secondary_off.loc[index]['Yards Gained']),#AV
                secondary_off.loc[index]['Play Type'],#AW
                secondary_off.loc[index]['Play Text'],#AX
                '',#AY
                '',#AZ
                '',#BA
                '',#BB
                '',#BC
                '',#BD
                f'=IF(AT{line}="","",IF(AT{line+1}="",AV{line},AT{line}-AT{line+1}))',#BE
                f'=BE{line}=AV{line}',#BF
                ]
        sheet.writerow(row)
        index+=1
        line+=1