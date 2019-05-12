import pandas as pd
import numpy as np
import statistics as st
import seaborn as sns
import matplotlib.pyplot as plt


from sklearn import preprocessing
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
from sklearn.svm import SVR

from sklearn.ensemble import RandomForestRegressor
from sklearn import neighbors
from sklearn.linear_model import ElasticNet
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold
from scipy.stats import norm
from operator import itemgetter

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from pandas.plotting import scatter_matrix
from sklearn import model_selection
from sklearn.metrics import classification_report
from yellowbrick.classifier import ClassificationReport





normalized = 0
rsampling = 0
year_holdout = 1
year_holdout = 2018

ABT = pd.read_csv("ABT.csv")
featuresUsed = ['G', 'MPG', 'PPG','RPG','APG', 'BLKPG', 'FG%', 'WS', 'VORP', 'followers', 'pagerank']
#ABT = ABT[featuresUsed]
ABT = ABT[ABT['Votes']!=0]
ABT = ABT[ABT['followers']!=0]


#ABT.plot.scatter(x = 'Votes', y = 'PPG')
#ABT.plot.scatter(x = 'Votes', y = 'MPG')
#ABT.plot.scatter(x = 'Votes', y = 'WS')
#plt.show()
#preprocessing
ABT.fillna(ABT.mean(), inplace = True)

if rsampling:
	target = ABT['Votes']
	data = ABT[featuresUsed]
	if normalized:
		data = (data-data.min()) / (data.max() - data.min())
	data_train, data_test, target_train, target_test = train_test_split(data,target, test_size = 0.25, random_state = 7)
if year_holdout:
	data_train = ABT[ABT['Year'] != year_holdout]
	data_train = data_train[featuresUsed]

	data_test = ABT[ABT['Year'] == year_holdout]
	data_test = data_test[featuresUsed]

	target_train = ABT[ABT['Year']!= year_holdout]
	target_train = target_train['Votes']

	target_test = ABT[ABT['Year'] == year_holdout]
	target_test = target_test['Votes']





def scoresRegression(model):
    
    model.fit(data_train, target_train)
    pred = model.predict(data_test)

    print("Mean squared error: %.3f" % mean_squared_error(pred, target_test))
    print('R2 score: %.3f' % r2_score(pred, target_test))

    cvScore = cross_val_score(model, data_test, target_test, cv = 3, scoring = 'r2')
    print("R2 cross validation score: %0.2f (+/- %0.2f)" % (cvScore.mean(), cvScore.std() * 2))

    #pred = [ '%.2f' % elem for elem in pred]
    df = pd.DataFrame({'Actual': target_test, 'Predicted': pred})
    df = df.sort_values('Predicted')
    print(df.head())
    for item in df['Predicted']:
    	index = df[df.Predicted == item].index[0]
    	#print(index)
    	#print(ABT.at[index, 'Player'])
    #print(df.head(20))



##test1
svr = SVR(kernel='rbf')
print('\n\n\n SVR:\n')
scoresRegression(svr)

print('\n\n RIDGE')
reg = linear_model.Ridge(alpha=.5)
scoresRegression(reg)

print('\n\n LASSO')
reg = linear_model.Lasso(alpha=.1)
scoresRegression(reg)

print('\n\n Elastic Net')
reg = ElasticNet(random_state = 0)
scoresRegression(reg)

print('\n\n KNN')
knn = neighbors.KNeighborsRegressor(n_neighbors = 7, weights = 'uniform')
scoresRegression(knn)

print('\n\n RF')
rf = RandomForestRegressor(random_state = 9, n_estimators = 100, criterion = 'mse')
scoresRegression(rf)



