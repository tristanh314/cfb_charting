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

    # # Collect a list of drive tables.
    drive_set = plays_soup.find_all('div', id='TableBase')

    # # Read the information from an html drive table into a pandas dataframe.
    plays_df = pd.DataFrame({'Offense':[],'Result':[],'Down_Dist':[], 'Description':[]})

    row_num = 0
    for drive in range(0, len(drive_set)):
        drive_off = find_off(drive_set[drive])
        drive_table = drive_set[drive].find('tbody')
        drive_plays = drive_table.find_all('tr')
        for index in range(0, len(drive_plays)):
            play_row = drive_plays[index].find_all('td')
            play_result = play_row[0].text
            play_desc = play_row[1].text
            down_dist = play_row[1].find('div').text
            plays_df.loc[row_num] = pd.Series({'Offense':drive_off, 'Result':play_result, 'Down_Dist':down_dist, 'Description':play_desc})
            row_num+=1

    # Split the plays into two dataframes, one for each team.
    ######################################################################################
    # This will need to be refactored to allow the teams to be determined by the script. #
    ######################################################################################
    team_A_df = plays_df[plays_df['Offense'] == 'IDAHO']
    team_B_df = plays_df[plays_df['Offense'] == 'NEVADA']
    
    return team_A_df, team_B_df

def parse_play(play):
    """
    Input: A dataframe of plays for a single team, eg, output of scrape_cbs.
    Output: A dataframe of values that can be written to an ATQ charting template.
    """

    # For each row in the input dataframe, parse the text scraped from CBS sports for result information.
    # for index in range(0, len(plays_df)):
    row = pd.Series({'E':'', 'F':np.NaN, 'G':'', 'AQ':np.NaN, 'AR':np.NaN, 'AS':np.NaN, 'AT':np.NaN, 'AV':np.NaN, 'AW':'', 'AX':''})
    if (re.compile('KICKOFF').search(play['Result']) != None) or (re.compile('PUNT').search(play['Result']) != None) or (re.compile('FIELD GOAL').search(play['Result'])):
        pass
    elif (re.compile('NO GAIN').search(play['Result'])) != None:
        row['AR'] = 0
    elif  (re.compile('\+[0-9]\s').search(play['Result'])) != None:
        row['AR'] = int(re.compile('\+[0-9]\s').search(play['Result']).group())
    elif  (re.compile('\-[0-9]\s').search(play['Result'])) != None:
        row['AR'] = int(re.compile('\-[0-9]\s').search(play['Result']).group())
    
    return row
# Print output to test script, comment out when not needed.
# drives = scrape_cbs('20230909_IDAHO@NEVADA_CBS.html')