#necessary imports to run the code
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os

"""A collection of function for doing my project."""

def combination(start_year, end_year):
    """
    Combines the nwsl.csv and position.csv csvs for each
    year in the given range ad
    
    :parameters:
    start_year - integer indicating start year of data
    end_year - integer indicating end year of data
    """
    for i in range(start_year, end_year + 1):
        nwsl_file = 'nwsl{}.csv'.format(i)
        position_file = 'position{}.csv'.format(i)

        nwsl = pd.read_csv(os.path.join('data', 'nwsl', nwsl_file))
        position = pd.read_csv(os.path.join('data', 'position', position_file))
        df = nwsl.merge(position, left_on='Player Name',
                            right_on='Player', how = 'left').drop('Player', axis = 1)

        name = 'full{}.csv'.format(i)
        path = os.path.join('data', 'full', name)

        df.to_csv(path, index=False)
    return

def calculate_stats(df):
    """
    Calculates Goals per Game, Assists per Game, Shots per Game, 
    Proportion of Shots on Goal per Goal, and Proportion of Shots on
    Goal, for each player in the dataset. Creates columns for these 
    values in each dataframe.
    
    :parameters:
    df - dataframe like nwsl.csv/full.csv with neceesary columns
    """
    #calculating stats, self explanatory column names
    df['Goals per Game'] = df['Goals']/df['Games Played']
    df['Assists per Game'] = df['Assists']/df['Games Played']
    df['Shots per Game'] = df['Shots']/df['Games Played']
    df['Prop SoG'] = df['Shots on Goal']/df['Shots']
    df['Shots per Goal'] = df['Goals']/df['Shots on Goal']
    
    int_cols = df.columns[2:].tolist()
    int_cols.remove('Position')
    for each in int_cols:
        df[each] = df[each].astype(float)
    
    #May create a classifer for Position later, leaving nulls in this column
    nonPos = df.loc[:, ~df.columns.isin(['Position'])].columns.tolist()
    df[nonPos] = df[nonPos].fillna(0)
    return