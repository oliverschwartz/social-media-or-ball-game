import pandas as pd
import numpy as np
import seaborn as sns
import glob
import networkx as nx
import matplotlib.pyplot as plt
import pylab
#from nba_scrape import NBA

from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression



# Read in all the data from Database. Delete all rows that correspond
# to players not on our list, or not from 2017 season. Additionally,
# delete the two blank columns
names = pd.read_csv('players-complete.csv', encoding='latin1')
names = names['name'].tolist()
df = pd.read_csv('Seasons_Stats.csv', encoding='latin1')
df = df.drop(columns = ['Unnamed: 0'])
df = df[df['Player'].isin(names)]
year = ['2017']
df = df[df['Year'].isin(year)]
df = df.drop(columns = ['blanl', 'blank2'])


# Read in data from nba.csv, nba_extra.csv (for 2018 and 2019 seasons).
# Clean up playername, merge the two csvs to match format above.
# Add year column and delete two blank rows. append the data 
# to dataframe above. Delete multiple entries for traded players
# Save in ABT.csv
seasons =["nba17-18", "nba18-19"]
for season in seasons:
    # Set variables
    file = season + "/nba.csv"
    file_extra = season + "/nba_extra.csv"
    year = 2000 + float(season[-2:])
    print(year)

    # Parse CSVs
    newSeason = pd.read_csv(file, encoding='latin1')
    newSeasonExtra = pd.read_csv(file_extra, encoding='latin1')
    newSeason = newSeason.drop(columns = ['Rk'])
    i = 0
    for name in newSeason['Player']:
        newSeason.loc[i, ['Player']] = name.split('\\')[0]
        i = i + 1

    for colName in newSeasonExtra.columns.tolist():
        if colName == 'FG':
            break
        newSeasonExtra.drop(columns = [colName], inplace = True)
    stats = pd.concat([newSeason, newSeasonExtra], axis = 1, join = 'inner')
    stats.insert(loc = 0, column = 'Year',value = year)
    stats.insert(loc = 6, column = 'GS', value = 'N/A')
    stats.drop(columns = ['Unnamed: 19', 'Unnamed: 24'], inplace = True)
    
    if year == 2018:
        fullStats = pd.concat([df, stats], ignore_index=True)
    else: 
        fullStats = pd.concat([fullStats, stats], ignore_index=True)
    current_player = ''
    for index, playername in enumerate(fullStats['Player']):
        if current_player == playername:
            fullStats.drop(index, inplace = True)
        current_player = playername

fullStats.to_csv('ABT.csv', index = False)


