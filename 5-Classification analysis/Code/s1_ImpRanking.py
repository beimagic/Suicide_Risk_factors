
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from collections import Counter
pd.options.mode.chained_assignment = None  # default='warn'

def normal_imp(mydict):
    mysum = sum(mydict.values())
    mykeys = mydict.keys()
    for key in mykeys:
        mydict[key] = mydict[key]/mysum
    return mydict

dpath = '/Volumes/JasonWork/Projects/OtherProjects/ZhangBei/'
data_df = pd.read_csv(dpath + 'Data/PredictorsData.csv')
my_f_lst = data_df.columns.tolist()[1:]
target_df = pd.read_csv(dpath + 'Data/TargetInfo.csv')
field_dict_df = pd.read_csv(dpath + 'Data/FeatureDict.csv', usecols = ['FieldID', 'FieldName'])
mydf = pd.merge(target_df, data_df, how = 'inner', on = ['eid'])

region_fold_lst = list(set(mydf.region_cv_fold))
inner_cv_fold_lst = list(set(mydf.in_cv_fold))

for region_fold in region_fold_lst:
    traindf = mydf.loc[mydf.region_cv_fold != region_fold]
    traindf.reset_index(inplace = True, drop = True)
    tg_imp_cv = Counter()
    for inner_cv_fold_id in inner_cv_fold_lst:
        in_train_idx = traindf['in_cv_fold'].index[traindf['in_cv_fold'] != inner_cv_fold_id]
        in_cv_X_train, in_cv_y_train = traindf.iloc[in_train_idx][my_f_lst], traindf.iloc[in_train_idx].target_y
        my_lgb = LGBMClassifier(objective='binary', metric='auc', is_unbalance=True, verbosity=-1, seed=2023)
        my_lgb.set_params(**{'n_estimators': 500, 'max_depth': 15, 'num_leaves': 10,
                             'subsample': 0.7, 'learning_rate': 0.01, 'colsample_bytree': 0.7})
        my_lgb.fit(in_cv_X_train, in_cv_y_train)
        totalgain_imp = my_lgb.booster_.feature_importance(importance_type='gain')
        totalgain_imp = dict(zip(my_lgb.booster_.feature_name(), totalgain_imp.tolist()))
        tg_imp_cv += Counter(normal_imp(totalgain_imp))
    tg_imp_cv = normal_imp(tg_imp_cv)
    tg_imp_df = pd.DataFrame({'Feature': list(tg_imp_cv.keys()), 'Importance': list(tg_imp_cv.values())})
    tg_imp_df.sort_values(by='Importance', ascending=False, inplace=True)
    tg_imp_df['FieldID'] = [int(ele.split('-')[0]) for ele in tg_imp_df.Feature]
    tg_imp_df = pd.merge(tg_imp_df, field_dict_df, how='left', on=['FieldID'])
    tg_imp_df.to_csv(dpath + 'Results/Suicide/TestingFold_'+str(region_fold)+'/s1_Importance.csv', index=False)

print('finished')

