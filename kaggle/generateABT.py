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


playerVotes = 2

def findUsername(player, names: pd.DataFrame):
    for i, playerName in enumerate(names['Player']):
        if player == playerName:
            return(names.at[i, 'Username'])
    return 'none'

def findVotes(player, votes: pd.DataFrame):
    for index, playerName in enumerate(votes['Player']):
        if player == playerName:
            return(votes.at[index, 'Votes'])
    print('not found')
    return 0

def orderMetrics(fullStats: pd.DataFrame, sMetrics: pd.DataFrame, names: pd.DataFrame, votes17: pd.DataFrame, votes18: pd.DataFrame, votes19: pd.DataFrame):
    print('Start!!!')
    metrics = np.zeros([1500,7])
    newMets = pd.DataFrame(data = metrics, columns = ['Username', 'pagerank', 'eigen', 'load', 'betw', 'followers', 'Votes'])
    for index, player in enumerate(fullStats['Player']):
        username = findUsername(player, names)
        if username != 'none':
            for index2, sUsername in enumerate(sMetrics['username']):
                if sUsername == username:
                    newMets.loc[index, ['Username']] = sMetrics.at[index2, 'username']
                    newMets.loc[index, ['pagerank']] = sMetrics.at[index2, 'pagerank']
                    newMets.loc[index, ['eigen']] = sMetrics.at[index2, 'eigen']
                    newMets.loc[index, ['load']] = sMetrics.at[index2, 'load']
                    newMets.loc[index, ['betw']] = sMetrics.at[index2, 'betw']
                    newMets.loc[index, ['followers']] = sMetrics.at[index2, 'followers']
        else:
            newMets.loc[index, ['Username']] = 0
            newMets.loc[index, ['pagerank']] = 0
            newMets.loc[index, ['eigen']] = 0
            newMets.loc[index, ['load']] = 0
            newMets.loc[index, ['betw']] = 0
            newMets.loc[index, ['followers']] = 0

        if fullStats.at[index, 'Year'] == 2017:
            newMets.loc[index, ['Votes']] = findVotes(player, votes17)
        if fullStats.at[index, 'Year'] == 2018:
            newMets.loc[index, ['Votes']] = findVotes(player, votes18)
        if fullStats.at[index, 'Year'] == 2019:
            newMets.loc[index, ['Votes']] = findVotes(player, votes19)

    return newMets

def perGame(fullStats: pd.DataFrame):
    ppg = []
    rpg = []
    apg = []
    stl = []
    blk = []
    mpg = []
    for index, pts in enumerate(fullStats['PTS']):
        ppg.append(pts / fullStats.at[index, 'G'])
        rpg.append(fullStats.at[index, 'TRB'] / fullStats.at[index, 'G'])
        apg.append(fullStats.at[index, 'AST'] / fullStats.at[index, 'G'])
        stl.append(fullStats.at[index, 'STL'] / fullStats.at[index, 'G'])
        blk.append(fullStats.at[index, 'BLK'] / fullStats.at[index, 'G'])
        mpg.append(fullStats.at[index, 'MP'] / fullStats.at[index, 'G'])
    pgStats =pd.DataFrame(np.column_stack([ppg, rpg, apg, stl, blk, mpg]), 
                               columns=['PPG', 'RPG', 'APG', 'STLPG', 'BLKPG', 'MPG'])
    return pd.concat([fullStats, pgStats], axis = 1)


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
    #print(year)

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

#Add in social media metrics
names = pd.read_csv("../ig/scripts/names-username.csv")
names = names[['Player', 'Username']]
sMetrics = pd.read_csv("../ig/scripts/metrics.csv")
if playerVotes == 1:
    votes17 = pd.read_csv("../allstar-votes/player-votes/playervotes17.csv")
    votes18 = pd.read_csv("../allstar-votes/player-votes/playervotes18.csv")
    votes19 = pd.read_csv("../allstar-votes/player-votes/playervotes19.csv")
if playerVotes == 2:
    votes17 = pd.read_csv("../allstar-votes/vote-share/voteShare17.csv")
    votes18 = pd.read_csv("../allstar-votes/vote-share/voteShare18.csv")
    votes19 = pd.read_csv("../allstar-votes/vote-share/voteShare19.csv")
else:
    votes17 = pd.read_csv("../allstar-votes/votes/votes17.csv")
    votes18 = pd.read_csv("../allstar-votes/votes/votes18.csv")
    votes19 = pd.read_csv("../allstar-votes/votes/votes19.csv")
fullStats.reset_index(drop = True, inplace = True)
mediaMetrics = orderMetrics(fullStats, sMetrics, names, votes17, votes18, votes19)
fullStats = perGame(fullStats)
fullStats = pd.concat([fullStats, mediaMetrics], axis = 1)



if playerVotes == 1:
    fullStats.to_csv('ABTpvotes.csv', index = False)
if playerVotes == 2:
    fullStats.to_csv('ABTvoteShare.csv', index = False)
else:
    fullStats.to_csv('ABT.csv', index = False)


