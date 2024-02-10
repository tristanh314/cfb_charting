# Import Dependencies

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re

def find_off(drive_table):
    """
    Input: A BeautifulSoup object corresponding to a table of play information for a single drive from CBS cfb play-by-play.
    Output: The abbreviation of the team that is on offense during the drive in question.
    """
    team_tag = drive_table.find('a', class_='')
    team_link = team_tag.get('href')
    team_split = team_link.split('/')
    team_abbr = team_split[3]
    return team_abbr

def scrape_cbs(html_file):
    """
    Input: Relative file path for donwloaded html of college football plays from a game recorded at cbssports.com.
    Output: Dataframes containing the data for the home team's offensive and defensive plays. 
    """

    # Store html from the downloaded page as a soup object.
    page=open(html_file)
    plays_soup = BeautifulSoup(page.read(), 'html.parser')
    page.close()

    # Collect a list of drive tables.
    drive_set = plays_soup.find_all('div', id='TableBase')

    # Read the information from html drive tables into  pandas dataframes.
    drive_list = []

    for drive in range(0, len(drive_set)):
        drive_df = pd.DataFrame({'Offense':[],'Result':[],'Description':[]})
        drive_off = find_off(drive_set[drive])
        drive_table = drive_set[drive].find('tbody')
        drive_plays = drive_table.find_all('tr')
        for index in range(0, len(drive_plays)):
            play_row = drive_plays[index].find_all('td')
            play_result = play_row[0].text
            play_desc = play_row[1].text
            # down_dist = play_row[1].find('div').text
            drive_df.loc[len(drive_df.index)] = pd.Series({'Offense':drive_off, 'Result':play_result, 'Description':play_desc})
        drive_list += [drive_df]

    # Split the plays into two dataframes, one for each team.
    ######################################################################################
    # This will need to be refactored to allow the teams to be determined by the script. #
    ######################################################################################
    team_A_drive_list = [drive for drive in drive_list if drive['Offense'][0]=='IDAHO']
    team_B_drive_list = [drive for drive in drive_list if drive['Offense'][0]=='NEVADA']
    
    return team_A_drive_list, team_B_drive_list

def parse_play(play, team):
    """
    Input: A dataframe of plays for a single team, eg, output of scrape_cbs.
    Output: A dataframe of values that can be written to an ATQ charting template.
    """

    # Create a series to store information for the output row.
    row = pd.Series({'E':'', 'F':np.NaN, 'G':'', 'AQ':np.NaN, 'AR':np.NaN, 'AS':np.NaN, 'AT':np.NaN, 'AV':np.NaN, 'AW':'', 'AX':''})

    # Determine yardage gained/lost if appropriate and and write to the output row.
    if (re.compile('NO GAIN').search(play['Result'])) != None:
        row['AR'] = 0
    elif  (re.compile('\+').search(play['Result'])) != None:
        row['AR'] = int(re.compile('[0-9]*\s').search(play['Result']).group())
    elif  (re.compile('\-').search(play['Result'])) != None:
        row['AR'] = -int(re.compile('[0-9]*\s').search(play['Result']).group())
    # Try to fiter the case below on input, keep these lines just in case.
    # elif (re.compile('KICKOFF').search(play['Result']) != None) or (re.compile('PUNT').search(play['Result']) != None) or (re.compile('FIELD GOAL').search(play['Result']) != None):
    #     pass

    # extract, distance, and field position.
    # FIX THIS
    down_dist_fp_str = re.compile('.*[(]').match(play['Description']).group()
    down_dist_fp = re.compile('[0-9][0-9]?').findall(down_dist_fp_str)
    
    # Write the down in the proper output format.
    try:
        down = down_dist_fp[0]
    except:
        down = ''
    if down == '1':
        row['E'] = '1st'
    elif down == '2':
        row['E'] = '2nd'
    elif down == '3':
        row['E'] = '3rd'
    elif down == '4':
        row['E'] = '4th'
    else:
        row['E'] = '?'

    # Write the distance in the proper output format.
    try:
        dist = int(down_dist_fp[1])
    except:
        dist = 0
    row['F'] = dist

    # Write the field position in the proper output format.
    try:
        fp = int(down_dist_fp[2])
    except:
        fp = 0
    if re.compile(team).search(down_dist_fp_str) == None:
        row['AT'] = fp
    else:
        row['AT'] = 100 -fp

    return row
# Use below to test functions, comment out when not needed.
# drives = scrape_cbs('20230909_IDAHO@NEVADA_CBS.html')