
import numpy as np
import pandas as pd
from Utility.Training_Utilities import *
from Utility.DelongTest import delong_roc_test
from lightgbm import LGBMClassifier
import scipy.stats as stats
from sklearn.calibration import CalibratedClassifierCV
from sklearn.calibration import calibration_curve
pd.options.mode.chained_assignment = None  # default='warn'

def get_nb_f(mydf):
    p_lst = mydf.p_delong.tolist()
    i = 0
    while((p_lst[i]<0.05)|(p_lst[i+1]<0.05)|(p_lst[i+2]<0.05)):
        i+=1
    return i


def get_pred_probs(tmp_f, mydf, fold_id_lst, col_name):
    eid_lst, region_lst = [], []
    y_test_lst, y_pred_lst = [], []
    for fold_id in fold_id_lst:
        train_idx = mydf['Region_code'].index[mydf['Region_code'] != fold_id]
        test_idx = mydf['Region_code'].index[mydf['Region_code'] == fold_id]
        X_train, X_test = mydf.iloc[train_idx][tmp_f], mydf.iloc[test_idx][tmp_f]
        y_train, y_test = mydf.iloc[train_idx].target_y, mydf.iloc[test_idx].target_y
        my_lgb = LGBMClassifier(objective='binary', metric='auc', is_unbalance=False, n_jobs=4, verbosity=-1, seed=2020)
        my_lgb.set_params(**{'n_estimators': 500, 'max_depth': 15, 'num_leaves': 10,
                             'subsample': 0.7, 'learning_rate': 0.01, 'colsample_bytree': 0.7})
        my_lgb.fit(X_train, y_train)
        y_pred_prob = my_lgb.predict_proba(X_test)[:, 1].tolist()
        y_pred_lst += y_pred_prob
        y_test_lst += mydf.target_y.iloc[test_idx].tolist()
        eid_lst += mydf.eid.iloc[test_idx].tolist()
        region_lst += mydf.Region_code.iloc[test_idx].tolist()
    myout_df = pd.DataFrame([eid_lst, region_lst, y_test_lst, y_pred_lst]).T
    myout_df.columns = ['eid', 'Region_code', 'target_y', 'y_pred_' + col_name]
    myout_df[['eid', 'Region_code']] = myout_df[['eid', 'Region_code']].astype('int')
    return myout_df

ImpMethod = 'TotalGain'

dpath = '../'
outputfile = dpath + 'Results/Results_Pheno/s3_PredProbs.csv'
pheno_auc_df = pd.read_csv(dpath + 'Results/Results_Pheno/s2.0_AccAUC_' + ImpMethod + '.csv')
nb_f = get_nb_f(pheno_auc_df)
pheno_f_lst = pheno_auc_df.Pheno_code.tolist()[:nb_f]
data_df = pd.read_csv(dpath + 'Data/PredictorsData.csv')
target_df = pd.read_csv(dpath + 'Data/target.csv')
mydf = pd.merge(target_df, data_df, how = 'inner', on = ['eid'])
fold_id_lst = list(set(mydf.Region_code))

pred_df = get_pred_probs(pheno_f_lst, mydf, fold_id_lst, 'probs')
pred_df.to_csv(outputfile, index = False)

