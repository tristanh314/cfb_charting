# Import Dependencies

import pandas as pd
import lxml
import html5lib
import re
from bs4 import BeautifulSoup

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

    # Read the play by play tables into dataframes
    drive_tables = pd.read_html(html_file, attrs={'class':'TableBase-table'})
    print(drive_tables[0])

scrape_cbs('20230909_IDAHO@NEVADA.html')