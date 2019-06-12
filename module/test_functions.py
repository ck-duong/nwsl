#necessary imports to run the code
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os

os.chdir('..') #change to main project directory

"""
Test for my functions.
Can be run from the notebook.
"""

from functions import combination, calculate_stats

##
##

def test_combo():
    assert combination(2016, 2019) == None
    
def test_calc():
    test = pd.read_csv(os.path.join('data', 'full', 'full2016.csv'))
    assert calculate_stats(test) == None

def test_nwsl_scraper():
    #getting all of the full.csv files in the subdirectory
    file_path = os.path.join('data', 'nwsl')
    csvs = os.listdir(path = file_path)
    files = []
    #for loop to get all the full.csv paths
    for file in csvs:
        fp = os.path.join(file_path, file)
        files.append(fp)
    #should be list of 4 paths
    assert len(files) == 4
    
def test_standing_scraper():
    #getting all of the full.csv files in the subdirectory
    standings_path = os.path.join('data', 'standings')
    standings_csvs = os.listdir(path = standings_path)
    standings_files = []
    #for loop to get all the full.csv paths
    for file in standings_csvs:
        fp = os.path.join(standings_path, file)
        standings_files.append(fp)
    #for organization purposes later
    assert len(standings_files) == 4