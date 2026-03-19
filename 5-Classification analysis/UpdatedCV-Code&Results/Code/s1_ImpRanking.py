
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from collections import Counter
from tqdm import tqdm
pd.options.mode.chained_assignment = None  # default='warn'

def normal_imp(mydict):
    '''
    Function to standardize the importance scores, allowing all features to have sumed importance as 1
    Input: dictionary given a features as keys and importance as values
    Onput: dictionary with normalized importance scores
    '''
    mysum = sum(mydict.values())
    mykeys = mydict.keys()
    for key in mykeys:
        mydict[key] = mydict[key]/mysum
    return mydict

'''
Read the data and prepared feature dictionary
'''
dpath = '../'
data_df = pd.read_csv(dpath + 'Data/PredictorsData.csv')
my_f_lst = data_df.columns.tolist()[1:]
target_df = pd.read_csv(dpath + 'Data/TargetInfo.csv')
field_dict_df = pd.read_csv(dpath + 'Data/FeatureDict.csv', usecols = ['FieldID', 'FieldName'])
my_f_df = pd.DataFrame({'Feature':my_f_lst})
my_f_df['FieldID'] = [int(ele.split('-')[0]) for ele in my_f_df.Feature]
my_f_df = pd.merge(my_f_df, field_dict_df, how='left', on=['FieldID'])
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
    '''
    traindf = mydf.loc[mydf.region_cv_fold != region_fold]
    traindf.reset_index(inplace = True, drop = True)
    tg_imp_cv = Counter()
    for inner_cv_fold_id in tqdm(inner_cv_fold_lst):
        '''
        All analytical procedures were performed strictly follow regional cross-validation.
        Within each of the regional fold, performing an inner cross-validation to calculate the importance
        fit a lightGBM model as my_lgb
        '''
        in_train_idx = traindf['in_cv_fold'].index[traindf['in_cv_fold'] != inner_cv_fold_id]
        in_cv_X_train, in_cv_y_train = traindf.iloc[in_train_idx][my_f_lst], traindf.iloc[in_train_idx].target_y
        my_lgb = LGBMClassifier(objective='binary', metric='auc', is_unbalance=True, verbosity=-1, seed=2023)
        my_lgb.set_params(**{'n_estimators': 500, 'max_depth': 15, 'num_leaves': 10,
                             'subsample': 0.7, 'learning_rate': 0.01, 'colsample_bytree': 0.7})
        my_lgb.fit(in_cv_X_train, in_cv_y_train)
        '''
        calculate the importance score within each inner fold of data
        '''
        totalgain_imp = my_lgb.booster_.feature_importance(importance_type='gain')
        totalgain_imp = dict(zip(my_lgb.booster_.feature_name(), totalgain_imp.tolist()))
        '''
        calculate the summed importance score within each inner fold of data
        '''
        tg_imp_cv += Counter(normal_imp(totalgain_imp))
    '''
    Normalize the importance score and merge with feature dictionary
    Sort the features based on importance and saved under each TestingFold_*
    '''
    tg_imp_cv = normal_imp(tg_imp_cv)
    tg_imp_df = pd.DataFrame({'Feature': list(tg_imp_cv.keys()), 'Importance': list(tg_imp_cv.values())})
    tg_imp_df = pd.merge(tg_imp_df, my_f_df, how='right', on=['Feature'])
    tg_imp_df['Importance'] = tg_imp_df['Importance'].fillna(0)
    tg_imp_df.sort_values(by='Importance', ascending=False, inplace=True)
    tg_imp_df.to_csv(dpath + 'Results/Suicide/TestingFold_'+str(region_fold)+'/s1_Importance.csv', index=False)

print('finished')

