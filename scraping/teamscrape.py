import requests
from bs4 import BeautifulSoup
import pandas as pd

base = 'http://www.nwslsoccer.com'
teams = base + '/stats#teams'
pull = requests.get(teams)
html = pull.content
soup = BeautifulSoup(html, 'html.parser')

df = pd.DataFrame(columns = ['Player', 'Position'])

team_links = []

team_data = soup.find(id="teams-nav")
for link in team_data.find_all('a'):
    team_links.append(link.get('href'))

for team in team_links:
    team_url = base + team
    team_pull = requests.get(team_url)
    team_content = team_pull.content
    team_soup = BeautifulSoup(team_content, 'html.parser')
    
    roster = team_soup.find('table', 
                            {'class': 'table table-responsive roster-table nwsl-table col-xs-12 col-sm-12 col-md-12 col-lg-12'})
    team_stats = []
    statistic = roster.find_all('td', class_ = 'player-name')
    
    for each in statistic:
        stat = each.text
        team_stats.append(stat.rsplit(' ', 1))
    team_df = pd.DataFrame(team_stats, columns = ['Player', 'Position'])
    df = pd.concat([df, team_df], ignore_index=True)
    
df.to_csv('position.csv', index = False)