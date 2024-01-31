# Import Dependencies

import pandas as pd
from bs4 import BeautifulSoup

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

    # Scrape the name and abbreviation for the teams
    away_info = plays_soup.find('div', class_='hud-table-cell team-name-container full away')
    away_abbr = away_info.find('div', class_='abbr').text
    away_abbr = away_abbr.replace('\n', '')
    away_abbr = away_abbr.replace(' ', '')
    away_team = away_info.find('div', class_='city').text
    away_team = away_team.replace('\n', '')
    away_team = away_team.replace(' ', '')    
    
    home_info = plays_soup.find('div', class_='hud-table-cell team-name-container full home')
    home_abbr = home_info.find('div', class_='abbr').text
    home_abbr = home_abbr.replace('\n', '')
    home_abbr = home_abbr.replace(' ', '')
    home_team = home_info.find('div', class_='city').text
    home_team = home_team.replace('\n', '')
    home_team = home_team.replace(' ', '')

    # # Collect a list of drive tables.
    drive_set = plays_soup.find_all('div', id='TableBase')

    # # Read the information from an html drive table into a pandas dataframe.
    drive_table = drive_set[0].find('tbody')
    drive_plays = drive_table.find_all('tr')
    play_row = drive_plays[0].find_all('td')
    play_result = play_row[0].text
    play_down_dist = play_row[1].text

    # # Determine the offense for each drive.
    return play_result, play_down_dist


print(scrape_cbs('20230909_IDAHO@NEVADA_CBS.html'))