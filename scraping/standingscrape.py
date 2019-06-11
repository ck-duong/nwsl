"""NWSL Standings Stat Scraper

This script allows the user to scrape team standings data
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

base = "http://www.nwslsoccer.com/standings?season={}"

for i in range(2016, 2020):
    linked = base.format(i)
    pull = requests.get(linked)
    html = pull.content
    soup = BeautifulSoup(html, 'html.parser')
    
    #where the data is, looked through the site's html to get these
    stats = ['panel-cell rank', 'panel-cell team', 'panel-cell points',
             'panel-cell home', 'panel-cell away', 'panel-cell goals-for',
             'panel-cell goals-against', 'panel-cell goal-difference']
    
    #creating the list of lists of stats
    all_stats = []
    for category in stats:
        statistic = soup.find_all("div", class_= category)
        arr = []
        for each in statistic:
            stat = each.text.strip().replace('\n', ' ')
            if stat:
                arr.append(stat)
        all_stats.append(arr)
    
    #turning list of lists into dataframe
    df = pd.DataFrame(all_stats)
    df = df.transpose()
    df.columns = ['Rank', 'Team', 'Points', 'Home', 'Away', 'Goals For',
                 'Goals Against', 'Goal Difference']

    #Cleaning up columns to be more readable/easier to calculate with
    split_home = df['Home'].apply(lambda x: x.split('-'))
    df['Home Wins'] = split_home.apply(lambda x: x[0]).astype(int)
    df['Home Losses'] = split_home.apply(lambda x: x[1]).astype(int)
    df['Home Ties'] = split_home.apply(lambda x: x[2]).astype(int)

    split_away = df['Away'].apply(lambda x: x.split('-'))
    df['Away Wins'] = split_home.apply(lambda x: x[0]).astype(int)
    df['Away Losses'] = split_home.apply(lambda x: x[1]).astype(int)
    df['Away Ties'] = split_home.apply(lambda x: x[2]).astype(int)

    df['Overall Wins']  = df['Home Wins'] + df['Away Wins']
    df['Overall Losses']  = df['Home Losses'] + df['Away Losses']
    df['Overall Ties']  = df['Home Ties'] + df['Away Ties']

    team_name = df['Team'].apply(lambda x: x.rsplit(' ', 1))
    df['Full Team'] = team_name.apply(lambda x: x[0])
    df['Team'] = team_name.apply(lambda x: x[1])
    
    #FCKC is the only team without their abbreviation listed on the website HTML
    #This is to keep consistency with the other csvs
    df['Team'] = df['Team'].replace('City', 'KC')
    df['Full Team'] = df['Full Team'].replace('FC Kansas', 'FC Kansas City')

    df = df[['Rank', 'Full Team', 'Team', 'Points',
             'Overall Wins', 'Overall Losses', 'Overall Ties',
             'Home Wins', 'Home Losses', 'Home Ties',
             'Away Wins', 'Away Losses', 'Away Ties',
             'Goals For', 'Goals Against', 'Goal Difference'
            ]]
    
    df['Season'] = i

    name = 'standings{}.csv'.format(i)
    path = os.path.join('data', 'standings', name)

    df.to_csv(path, index=False)
    time.sleep(2)