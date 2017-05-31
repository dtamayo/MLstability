import pandas as pd
import numpy as np
import sklearn
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import roc_auc_score
from xgboost.sklearn import XGBClassifier
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
import pickle
import sys
from functools import partial
import xgboost as xgb
from xgboost import DMatrix


##################################################
#Need to edit hyperopt hp.quinform method in docs
#to actually return an int instead of float for this to work
##################################################


def load_data():
    path = sys.argv[1] #start from 1
    df = pd.read_csv(path, index_col = 0)
    return df


def clean_data(data):
    vals = ["instability_time","Rel_Eerr", "Rel_Eerr_short" , "runstring"]
    for val in vals:
        try:
            del data[val]
            
        except Exception as e:
            print e
        #print data
    return data
    


def objective(space, trainX, trainY):

    clf = XGBClassifier(n_estimators = 100, 
                            max_depth = space['max_depth'], 
                            min_child_weight =space['min_child_weight'],
                            subsample = space['subsample'],
                            colsample_bytree =space['colsample_bytree'],
                            learning_rate = space['learning_rate'])

    xgtrain = DMatrix(trainX.values, label = trainY.values)
    cv_result = xgb.cv(clf.get_params(), xgtrain, num_boost_round = 10, nfold = 5, metrics ='auc', early_stopping_rounds = 5) 

    score = cv_result.iloc[-1]["test-auc-mean"]
    score_std = cv_result.iloc[-1]["test-auc-std"]
    print "SCORE:", score

    return{'loss':1-score, 'status': STATUS_OK, "cv_score":score, "cv_avg":score_std  }




def optimize(data, iterations):
    
    #create holdout set now
    Nrows = int(data.shape[0])

    Y = data["Stable"]
    del data["Stable"]

    trainX = data.iloc[:Nrows, :]
    trainY = Y.iloc[:Nrows]
    testX = data.iloc[Nrows:, :]
    testY = Y.iloc[Nrows:]



    space = {"max_depth": hp.quniform("x_max_depth", 1, 10, 1),
    'min_child_weight': hp.quniform ('x_min_child', 1, 10, 1),
    'subsample': hp.uniform ('x_subsample', 0.8, 1),
    'colsample_bytree': hp.uniform ('x_tree_colsample', 0.5,1),
    'learning_rate': hp.uniform ('x_learning_rate', 0.001, 0.1),
    #'trainX': trainX, 'trainY':trainY
    }



    trials3 = Trials()
    optimize_func = partial(objective, trainX= trainX, trainY =trainY)
    best = fmin(fn = optimize_func, space = space, algo= tpe.suggest, max_evals = iterations)
    #this will print out the score at each iteration, can pipe it to a text file to save it for later
    data_pieces = [trainX, trainY, testX, testY]
    return best, data_pieces


def save_model_parameters(save_name, parameters, data_pieces):
    trainX, trainY, testX, testY = data_pieces
    model = XGBClassifier()
    model.fit(trainX, trainY)
    pickle.dump(model, open(save_name+"model.pkl", 'wb'))
    pickle.dump(parameters,open(save_name+"params.pkl", "wb"))    
    return
    



if __name__ == "__main__":
    #do something
    data = load_data()
    #dont know if this is actually needed, I would assume that I would use all the feauters available to me 
    data = clean_data(data)
    # def get_data():
    #     new_data = data[:,:]
    #    return new_data# =data[:,:] # not an alias
    try:
        iterations = int(sys.argv[2])
    except:
        iterations = 10
    parameters , data_pieces = optimize(data, iterations)
    
    #save parameters and trained model with holdout set
    save_name = sys.argv[3]
    
    save_model_parameters(save_name, parameters, data_pieces) 






