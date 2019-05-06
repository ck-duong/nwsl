import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

soccer = "http://www.nwslsoccer.com/stats#players"
pull = requests.get(soccer)
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
df = df.dropna() #remove team data

df.to_csv('nwsl.csv', index=False)