"""NWSL Player Position Scraper

This script allows the user to scrape player stat data
from the official NWSL website, specifically from their
team's roster page, from 2016 - 2019, but can be modified
to scrape a different range of years.

This script requires that the packages imported below be installed 
within the Python environment you are running this script in.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import os

base = 'http://www.nwslsoccer.com'
teams = base + '/stats#teams'
pull = requests.get(teams)
html = pull.content
soup = BeautifulSoup(html, 'html.parser')

team_links = []

team_data = soup.find(id="teams-nav")
for link in team_data.find_all('a'):
    team_links.append(link.get('href'))

for i in range(2016, 2020):
    df = pd.DataFrame(columns = ['Player', 'Position'])
    
    for team in team_links:
        team_url = "http://www.nwslsoccer.com{}?statsType=team&statsSeason=2019&scheduleSeason=2019&rosterSeason={}&psort=#roster".format(team, i)
        team_pull = requests.get(team_url)
        
        team_content = team_pull.content
        team_soup = BeautifulSoup(team_content, 'html.parser')
        if team_soup.find('h2', {'class' : 'error__code'}):
            break
                
        roster = team_soup.find('table', 
                                {'class': 'table table-responsive roster-table nwsl-table col-xs-12 col-sm-12 col-md-12 col-lg-12'})
        team_stats = []
        statistic = roster.find_all('td', class_ = 'player-name')

        for each in statistic:
            stat = each.text
            team_stats.append(stat.rsplit(' ', 1))
            
        team_df = pd.DataFrame(team_stats, columns = ['Player', 'Position'])
        df = pd.concat([df, team_df], ignore_index=True)

        name = 'position{}.csv'.format(i)
        path = os.path.join('data', 'position', name)

        df.to_csv(path, index=False)
        time.sleep(2)