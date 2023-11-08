import numpy as np
import pandas as pd
import openpyxl as op

############# USER INPUT REQUIRED #############
# INPUT RELATIVE PATH TO RAW DATA
game_data = pd.read_csv('asu_wsu_raw.csv')
# INPUT RELATIVE PATH TO DESTINATION FILE
file_name = "ASU_WSU_TH.ods"
# SPECIFY NAMES AND ABBREVIATIONS TO USE.
game_num = 5
prime_team = "Arizona State"
sec_team = "Washington State"
prime_abrev = "ASU"
sec_abrev  = "WSU"
######### DID YOU CHECK YOUR CHOICES? #########

# Remove information that will not be used.
game_data = game_data.drop(columns=['Id','Offense Conference','Defense Conference','Home','Away','Game Id','Drive Id','Offense Timeouts','Defense Timeouts','Yard Line','Ppa','Wallclock'])

i=0
frame_length=game_data.shape[0]
while i < frame_length:
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

# Load the template
wb = op.load_workbook(filename = 'atq_charting_template.xlsx')
# print(wb.sheetnames)

#Enter data for primary offense 
ws = wb['PRIME Off, SEC Def']
ws.title = f'{prime_abrev} Offense, {sec_abrev} Offense'
index = 0
t_row = 1
# print(ws)
while index < primary_off.shape[0]:
    row = primary_off.iloc[index]
    ws[f'A{t_row}']=game_num
    ws[f'B{t_row}']=prime_abrev
    ws[f'D{t_row}']='O'
    ws[f'E{t_row}']=down_string(int(row['Down']))
    ws[f'F{t_row}']=int(row['Distance'])
    ws[f'G{t_row}']=row['Play Abrev']
    ws[f'AN{t_row}']=int(row['Offense Score'])
    ws[f'AO{t_row}']=int(row['Defense Score'])
    ws[f'AQ{t_row}']=int(row['Period'])
    ws[f'AR{t_row}']=int(row['Clock Minutes'])
    ws[f'AS{t_row}']=int(row['Clock Seconds'])
    ws[f'AT{t_row}']=int(row['Yards To Goal'])
    ws[f'AV{t_row}']=int(row['Yards Gained'])
    ws[f'AW{t_row}']=row['Play Type']
    ws[f'AX{t_row}']=row['Play Text']
#   Skip rows in necessary
    if index == primary_off.shape[0]-1:
        pass
    elif primary_off.loc[index]['Drive Number'] != primary_off.loc[index+1]['Drive Number']:
        t_row+=2
    else:
        t_row+=1
#   Iterate the index 
    index+=1

#Enter data for secondary offense 
ws = wb['SEC Off, PRIME Def']
ws.title = f'{sec_abrev} Offense, {prime_abrev} Offense'
index = 0
t_row = 1
# print(ws)
while index < secondary_off.shape[0]:
    row = secondary_off.iloc[index]
    ws[f'A{t_row}']=game_num
    ws[f'B{t_row}']=prime_abrev
    ws[f'D{t_row}']='ddd'
    ws[f'E{t_row}']=down_string(int(row['Down']))
    ws[f'F{t_row}']=int(row['Distance'])
    ws[f'G{t_row}']=row['Play Abrev']
    ws[f'AN{t_row}']=int(row['Offense Score'])
    ws[f'AO{t_row}']=int(row['Defense Score'])
    ws[f'AQ{t_row}']=int(row['Period'])
    ws[f'AR{t_row}']=int(row['Clock Minutes'])
    ws[f'AS{t_row}']=int(row['Clock Seconds'])
    ws[f'AT{t_row}']=int(row['Yards To Goal'])
    ws[f'AV{t_row}']=int(row['Yards Gained'])
    ws[f'AW{t_row}']=row['Play Type']
    ws[f'AX{t_row}']=row['Play Text']
#   Skip rows in necessary
    if index == secondary_off.shape[0]-1:
        pass
    elif secondary_off.loc[index]['Drive Number'] != secondary_off.loc[index+1]['Drive Number']:
        t_row+=2
    else:
        t_row+=1
#   Iterate the index 
    index+=1

# Save the modified workbook as .xlsx
wb.save('experiment.xlsx')