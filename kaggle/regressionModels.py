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
from scipy.stats import shapiro
from statsmodels.stats import stattools as stools



targ = 'Votes'


normalized = 0
rsampling = 0
year_holdout = 1
year_holdout = 2019
playerVotes = 2 #0 for votes, 1 for player votes, 2 for normal vote share

if playerVotes == 1:
	ABT = pd.read_csv("ABTpvotes.csv")
if playerVotes == 2:
	ABT = pd.read_csv("ABTvoteShare.csv")
else:
	ABT = pd.read_csv("ABT.csv")
featuresUsed = ['G', 'MPG', 'PPG','RPG','APG', 'BLKPG', 'FG%', 'WS', 'VORP', 'followers', 'pagerank']
featuresUsed = ['G', 'MPG', 'PPG','RPG','APG', 'BLKPG', 'FG%', 'WS', 'VORP']
ABT = ABT[ABT[targ]!=0]
ABT = ABT[ABT['followers']!=0]



#ABT.plot.scatter(x = targ, y = 'PPG')
#ABT.plot.scatter(x = targ, y = 'MPG')
#ABT.plot.scatter(x = targ, y = 'WS')
#plt.show()
#preprocessing
ABT.fillna(ABT.mean(), inplace = True)

if rsampling:
	target = ABT[targ]
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
	target_train = target_train[[targ]]


	target_test = ABT[ABT['Year'] == year_holdout]
	target_test2 = target_test[targ]
	target_test = target_test[[targ]]
	if normalized:
		data_train = (data_train-data_train.min()) / (data_train.max() - data_train.min())
		data_test = (data_test-data_test.min()) / (data_test.max() - data_test.min())

	
print ()




def scoresRegression(y, model):
    
    model.fit(data_train, target_train.values.ravel())
    pred = model.predict(data_test)

    print("Mean squared error: %.3f" % mean_squared_error(target_test, pred))
    print('R2 score: %.3f' % r2_score(target_test, pred))

    cvScore = cross_val_score(model, data_test, target_test.values.ravel(), cv = 3, scoring = 'r2')
    #cvScore = cross_val_score(model, data_test, target_test, cv = 3, scoring = 'r2')
    print("R2 cross validation score: %0.2f (+/- %0.2f)" % (cvScore.mean(), cvScore.std() * 2))

    #pred = [elem for elem in pred]
    df = pd.DataFrame({'Actual': target_test2, 'Predicted': pred})
    #print(df.head(10))
    df = df.sort_values('Predicted')
    for item in df['Predicted']:
    	index = df[df.Predicted == item].index[0]
    	#print(index)
    	print(ABT.at[index, 'Player'])
    #print(df.h(20))
    for i in pred:
    	y.append(i)



##test1
y_svr = []
svr = SVR(kernel='linear')
#print('\n\n\n SVR:\n')
#scoresRegression(y_svr, svr)

y_ridge = []
print('\n\n RIDGE')
reg = linear_model.Ridge(alpha=.5)
scoresRegression(y_ridge, reg)

y_Lasso = []
print('\n\n LASSO')
reg = linear_model.Lasso(alpha=.1)
scoresRegression(y_Lasso, reg)

y_EN = []
print('\n\n Elastic Net')
reg = ElasticNet(random_state = 0)
scoresRegression(y_EN, reg)

y_knn = []
print('\n\n KNN')
knn = neighbors.KNeighborsRegressor(n_neighbors = 7, weights = 'uniform')
scoresRegression(y_knn, knn)

y_rf = []
print('\n\n RF')
rf = RandomForestRegressor(random_state = 9, n_estimators = 100, criterion = 'mse')
scoresRegression(y_rf, rf)
#print(y_rf)

def residuals(x, y):
    #print(target_test.head())
    resid = [i for i in (target_test[targ] - x)]
    ssr = [i ** 2 for i in resid]
    
    ssrSum = 0
    for i in ssr:
        ssrSum += i
        
    standResid = []
    for i in resid:
        standResid.append(i / ((ssrSum / (target_test.shape[0] - 2)) ** (1/2)))
    
    for i in standResid:
        y.append(i)


#residuals
svrResid = []
rfResid = []
knnResid = []
ridgeResid = []
lassoResid =[]
ENResid = []
print('\n\n\n AQUIIIIII\n\n')
#residuals(y_svr, svrResid)
residuals(y_rf, rfResid)
residuals(y_knn, knnResid)
residuals(y_ridge, ridgeResid)
residuals(y_Lasso, lassoResid)
residuals(y_EN, ENResid)

#shapiro wilkes
#print(shapiro(svrResid))
print(shapiro(rfResid))
print(stools.durbin_watson(rfResid))
print('\n\n')
print(shapiro(knnResid))
print(stools.durbin_watson(knnResid))
print('\n\n')
print(shapiro(ridgeResid))
print(stools.durbin_watson(ridgeResid))
print('\n\n')
print(shapiro(lassoResid))
print(stools.durbin_watson(lassoResid))
print('\n\n')
print(shapiro(ENResid))
print(stools.durbin_watson(ENResid))

#DW test



