
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
import pickle
from tqdm import tqdm
pd.options.mode.chained_assignment = None  # default='warn'

'''
Read the data and prepared feature dictionary
'''
dpath = '../'
data_df = pd.read_csv(dpath + 'Data/PredictorsData.csv')
my_f_lst = data_df.columns.tolist()[1:]
target_df = pd.read_csv(dpath + 'Data/TargetInfo.csv')
field_dict_df = pd.read_csv(dpath + 'Data/FeatureDict.csv', usecols = ['FieldID', 'FieldName'])
mydf = pd.merge(target_df, data_df, how = 'inner', on = ['eid'])
'''
region_fold_lst: 0-9, indicating the region of participants' visiting center
inner_cv_fold_lst: 0-9, ten folds of inner cross-validation within each regional fold, which was pre-assigned
'''
region_fold_lst = list(set(mydf.region_cv_fold))
inner_cv_fold_lst = list(set(mydf.in_cv_fold))

for region_fold in tqdm(region_fold_lst):
    '''
    For regional cross validation, merely using the training data (nine regional fold of data) to train the model
    Save the trained models
    Get predicted risks in the testing data (remaining regional fold)
    '''
    traindf = mydf.loc[mydf.region_cv_fold != region_fold]
    traindf.reset_index(inplace = True, drop = True)
    testdf = mydf.loc[mydf.region_cv_fold == region_fold]
    testdf.reset_index(inplace = True, drop = True)
    auc_imp_df = pd.read_csv(dpath + 'Results/Suicide/TestingFold_' + str(region_fold) + '/s2.0_sf_selection.csv')
    '''
    We naively using the top-10 features which was consistent across each regional cross validation set 
    '''
    nb_f = 10
    my_f_lst = auc_imp_df.Feature.tolist()[:nb_f]
    cv_X_train,cv_X_test = traindf[my_f_lst], testdf[my_f_lst]
    cv_y_train, cv_y_test = traindf.target_y, testdf.target_y
    '''
    Model establishment using training set
    '''
    my_lgb = LGBMClassifier(objective='binary', metric='auc', is_unbalance=False, n_jobs=4, verbosity=-1, seed=2020)
    my_lgb.set_params(**{'n_estimators': 500, 'max_depth': 15, 'num_leaves': 10,
                         'subsample': 0.7, 'learning_rate': 0.01, 'colsample_bytree': 0.7})
    my_lgb.fit(cv_X_train, cv_y_train)
    '''
    Saving models
    '''
    with open(dpath + 'Results/Suicide/TestingFold_'+str(region_fold)+'/s3.1_top'+str(nb_f)+'_features_trained_model.pkl', 'wb') as f:
        pickle.dump(my_lgb, f)
    '''
    Getting predicted risks using the testing regional fold and save the predicted risks
    '''
    cv_y_pred = my_lgb.predict_proba(cv_X_test)[:, 1].tolist()
    pred_df = pd.DataFrame({'eid':testdf.eid.tolist(), 'target_y':testdf.target_y.tolist(), 'y_pred_probs':cv_y_pred})
    pred_df = pd.merge(pred_df, mydf[['eid', 'region_cv_fold', 'in_cv_fold']], how = 'left', on = 'eid')
    pred_df.to_csv(dpath + 'Results/Suicide/TestingFold_'+str(region_fold)+'/s3.1_top'+str(nb_f)+'_features_predicted_risks.csv', index = False)


