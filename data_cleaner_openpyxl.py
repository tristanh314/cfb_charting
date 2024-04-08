import numpy as np
import pandas as pd
import openpyxl as op
import sys
import re
import datetime as dt

# Determine the names of the teams in the game.
def get_teams(row):
    """
    Input: A series taken from any row in the dataframe read from a .csv download of play data. Typically the first row.
    Output: The names of both teams, one determined by user input, playing in the game.
    """
    while True:
        prime = input('Team of record: ')
        if row['Offense'] == prime:
            break
        elif row['Defense'] == prime:
            break
        else:
            print('Team of record not found, check spelling.')
    return prime

def abbrev(string):
    """
    Input: A 'Play Type' entry from collegefootballstats.com play data.
    Output: A one letter abbreviation for the type of play.
    """
    if re.compile('Pass').search(string) != None:
        return 'p'
    elif re.compile('Sack').search(string) != None:
        return 'p'
    elif re.compile('Rush').search(string) != None:
        return 'r'
    else:
        return '?'
    
def filter_plays(plays_df):
    """
    Input: A datframe read from a .csv file of college football plays.
    Output: The input dataframe less all rows that are not an offense running a play against a defense.
    """

    game_data = plays_df.drop(columns=['Id','Offense Conference','Defense Conference','Home','Away','Game Id','Drive Id','Offense Timeouts','Defense Timeouts','Yard Line','Ppa'])

    i=0
    frame_length=game_data.shape[0]
    while i < frame_length:
        if re.compile('Kickoff').search(game_data.loc[i]['Play Type']) != None:
            game_data.drop(index=i, inplace=True)
        elif re.compile('Punt').search(game_data.loc[i]['Play Type']) != None:
            game_data.drop(index=i, inplace=True)
        elif re.compile('Field Goal').search(game_data.loc[i]['Play Type']) != None:
            game_data.drop(index=i, inplace=True)
        elif re.compile('Timeout').search(game_data.loc[i]['Play Type']) != None:
            game_data.drop(index=i, inplace=True)
        elif re.compile('End').search(game_data.loc[i]['Play Type']) != None:
            game_data.drop(index=i, inplace=True)
        i+=1

    # Sort the plays by date and time
    game_data['Date'] = game_data['Wallclock'].apply(lambda x: dt.datetime.strptime(x[0:10], '%Y-%m-%d').date())
    game_data.drop(columns=['Wallclock'], inplace=True)
    game_data.sort_values(by=['Date', 'Drive Number', 'Play Number'])

    # Create appropriate play abbreviations
    abreviations = game_data['Play Type'].appy(abbrev)
    game_data['Play Abrev'] = abreviations
    
    # Reset the index of the dataframe
    game_data.reset_index(drop=True, inplace=True)

    return game_data

def col_k(play_type, play_text):
    """
    Input: The 'Play Type' and 'Play Text' (in order) etnried from a line in the .csv play data from collegefootballstats.
    Output: An apporpriate one-character code for penalties, touchdowns, turnovers, and two point conversions.
    """
    if re.compile('Touchdown').search(play_type) != None:
        if re.compile('two-point').search(play_text) != None:
            return '?'
        else:
            return 't'
    elif re.compile('Interception').search(play_type) != None:
        return 'x'
    elif re.compile('Fumble Recovery [()]Opponent[)]').search(play_type) != None:
        return 'x'
    elif re.compile('Penalty').search(play_type) != None:
        return '?'   
    else:
        return ''

def down_string(down):
    """
    Input: An integer represnting the down number.
    Output: A string representing the down number for data type coherency.
    """
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

def main(template_file='', data_list=list):
    """
    Input: Aan .xlsx to use a template to write data, a list of .csv files with college football play data from collegfootballdata.com, and a name for the .xlsx file to output
    the written data to.
    Output: Returns none, saves a copy of the play data written to the .xlsx template.
    """
    # User inputs name of the output file.
    output_file = input('Name of spreasheet to save (leave off file suffix): ')

    # Read the data from the .csv data files, concatenate into a single dataframe, and process the plays.
    games_list = [pd.read_csv(data_file) for data_file in data_list]
    combined_games = pd.concat(games_list, ignore_index=True)
    game_data = filter_plays(combined_games)

    # Sort play data by team on offense.
    prime = get_teams(game_data.loc[0])
    primary_off_df = game_data.loc[game_data['Offense']==prime].reset_index(drop=True)
    secondary_off_df = game_data.loc[game_data['Defense']==prime].reset_index(drop=True)

    # Load the template
    wb = op.load_workbook(filename = template_file)

    # Enter data for primary offense 
    ws_1 = wb['PRIME Off']
    ws_1.title = f'{prime} Offense'
    index = 0
    t_row = 1
    # print(ws)
    while index < primary_off_df.shape[0]:
        row = primary_off_df.loc[index]
        ws_1[f'A{t_row}']=row['Date']
        ws_1[f'B{t_row}']=row['Defense']
        ws_1[f'E{t_row}']=down_string(int(row['Down']))
        ws_1[f'F{t_row}']=int(row['Distance'])
        ws_1[f'G{t_row}']=row['Play Abrev']
        ws_1[f'K{t_row}']=col_k(row['Play Type'], row['Play Text'])
        ws_1[f'AN{t_row}']=int(row['Offense Score'])
        ws_1[f'AO{t_row}']=int(row['Defense Score'])
        ws_1[f'AQ{t_row}']=int(row['Period'])
        ws_1[f'AR{t_row}']=int(row['Clock Minutes'])
        ws_1[f'AS{t_row}']=int(row['Clock Seconds'])
        ws_1[f'AT{t_row}']=int(row['Yards To Goal'])
        ws_1[f'AV{t_row}']=int(row['Yards Gained'])
        ws_1[f'AW{t_row}']=row['Play Type']
        ws_1[f'AX{t_row}']=row['Play Text']
    #   Skip rows in necessary
        if index == primary_off_df.shape[0]-1:
            pass
        elif primary_off_df.loc[index]['Drive Number'] != primary_off_df.loc[index+1]['Drive Number']:
            ws_1[f'A{t_row+1}']=row['Date']
            ws_1[f'B{t_row+1}']=row['Defense']
            t_row+=2
        else:
            t_row+=1
    #   Iterate the index 
        index+=1

    #Enter data for secondary offense 
    ws_2 = wb['PRIME Def']
    ws_2.title = f'{prime} Defense'
    index = 0
    t_row = 1
    # print(ws)
    while index < secondary_off_df.shape[0]:
        row = secondary_off_df.loc[index]
        ws_2[f'A{t_row}']=row['Date']
        ws_2[f'B{t_row}']=row['Offense']
        ws_2[f'E{t_row}']=down_string(int(row['Down']))
        ws_2[f'F{t_row}']=int(row['Distance'])
        ws_2[f'G{t_row}']=row['Play Abrev']
        ws_2[f'K{t_row}']=col_k(row['Play Type'], row['Play Text'])
        ws_2[f'AN{t_row}']=int(row['Offense Score'])
        ws_2[f'AO{t_row}']=int(row['Defense Score'])
        ws_2[f'AQ{t_row}']=int(row['Period'])
        ws_2[f'AR{t_row}']=int(row['Clock Minutes'])
        ws_2[f'AS{t_row}']=int(row['Clock Seconds'])
        ws_2[f'AT{t_row}']=int(row['Yards To Goal'])
        ws_2[f'AV{t_row}']=int(row['Yards Gained'])
        ws_2[f'AW{t_row}']=row['Play Type']
        ws_2[f'AX{t_row}']=row['Play Text']
    #   Skip rows in necessary
        if index == secondary_off_df.shape[0]-1:
            pass
        elif secondary_off_df.loc[index]['Drive Number'] != secondary_off_df.loc[index+1]['Drive Number']:
            ws_2[f'A{t_row+1}']=row['Date']
            ws_2[f'B{t_row+1}']=row['Offense']
            t_row+=2
        else:
            t_row+=1
    #   Iterate the index 
        index+=1

    # Save the modified workbook as .xlsx
    wb.save(f'{output_file}.xlsx')

    return None

if __name__ == '__main__':
    main(template_file='atq_charting_template.xlsx', data_list=sys.argv[1:])