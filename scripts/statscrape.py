"""Individual NWSL Player Stat Scraper
This script allows the user to scrape player stat data
from the official NWSL website from 2016 - 2019, but
can be modified to scrape a different range of years.
This script requires that the packages imported below be installed 
within the Python environment you are running this script in.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import os

soccer = "http://www.nwslsoccer.com/stats?season={}#players"
for i in range(2016, 2020):
    linked = soccer.format(i)
    pull = requests.get(linked)
    html = pull.content
    soup = BeautifulSoup(html, 'html.parser')

    #print(soup.prettify())

    stats = ['player-name', '', 'gp', 'gs', 'mins', 'g current', 'a',
    's', 'sog', 'fc', 'off', 'ck', 'pka', 'pkg', 'yc', 'rc']
    all_stats = []
    for category in stats: #replace with function, apply. #TODO
        statistic = soup.find_all("td", class_= category)
        arr = []
        for each in statistic:
            stat = each.text.strip().replace('\n', ' ')
            arr.append(stat)
        all_stats.append(arr)

    df = pd.DataFrame(all_stats)
    df = df.transpose()
    df.columns = ['Player Name', 'Team', 'Games Played', 'Games Started', 'Minutes Played', 'Goals',
    'Assists', 'Shots', 'Shots on Goal', 'Fouls Committed', 'Offsides', 'Corner Kicks',
    'Penalty Kicks Attempted', 'Penalty Kick Goals', 'Yellow Cards', 'Red Cards']
    
    df['Team'] = df['Team'].replace('', 'KC') #recent NWSL update removed KC from the player HTML
    df['Season'] = i #add the year for later reference
    
    df = df.dropna() #remove team data

    name = 'nwsl{}.csv'.format(i)
    path = os.path.join('data', 'nwsl', name)

    df.to_csv(path, index=False)
    time.sleep(2)