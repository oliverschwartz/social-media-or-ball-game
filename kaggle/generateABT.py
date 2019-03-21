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

def draw_missing_data_table(df):
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    return missing_data

# Plot learning curve
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Validation score")

    plt.legend(loc="best")
    return plt

# Plot validation curve
def plot_validation_curve(estimator, title, X, y, param_name, param_range, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    train_scores, test_scores = validation_curve(estimator, X, y, param_name, param_range, cv)
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    plt.plot(param_range, train_mean, color='r', marker='o', markersize=5, label='Training score')
    plt.fill_between(param_range, train_mean + train_std, train_mean - train_std, alpha=0.15, color='r')
    plt.plot(param_range, test_mean, color='g', linestyle='--', marker='s', markersize=5, label='Validation score')
    plt.fill_between(param_range, test_mean + test_std, test_mean - test_std, alpha=0.15, color='g')
    plt.grid() 
    plt.xscale('log')
    plt.legend(loc='best') 
    plt.xlabel('Parameter') 
    plt.ylabel('Score') 
    plt.ylim(ylim)


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


# Read in data from nba.csv, nba_extra.csv (for 2018 season).
# Clean up playername, merge the two csvs to match format above.
# Add year column and delete two blank rows. append the data 
# to dataframe above. Delete multiple entries for traded players
# Save in ABT.csv
newSeason = pd.read_csv('nba17-18/nba.csv', encoding='latin1')
newSeasonExtra = pd.read_csv('nba17-18/nba_extra.csv', encoding='latin1')
newSeason = newSeason.drop(columns = ['Rk'])
i = 0
for name in newSeason['Player']:
    newSeason.loc[i, ['Player']] = name.split('\\')[0]
    i = i + 1

for colName in newSeasonExtra.columns.tolist():
    if colName == 'FG':
        break
    newSeasonExtra.drop(columns = [colName], inplace = True)
stats18 = pd.concat([newSeason, newSeasonExtra], axis = 1, join = 'inner')
stats18.insert(loc = 0, column = 'Year',value = 2018.0)
stats18.insert(loc = 6, column = 'GS', value = 'N/A')
stats18.drop(columns = ['Unnamed: 19', 'Unnamed: 24'], inplace = True)
fullStats = pd.concat([df, stats18], ignore_index=True)
current_player = ''
for index, playername in enumerate(fullStats['Player']):
    if current_player == playername:
        fullStats.drop(index, inplace = True)
    current_player = playername

fullStats.to_csv('ABT.csv', index = False)


# for testing purposes
dfList = df.columns.tolist()
stats18List = stats18.columns.tolist()
print("in df not in new:")
for feature in dfList:
    if feature not in stats18List:
        print (feature)
print("in new not df:")
for feature in stats18List:
    if feature not in dfList:
        print (feature)

#random tests:
#league = NBA()

#newStats = pd.concat([df, stats18], ignore_index=True)
