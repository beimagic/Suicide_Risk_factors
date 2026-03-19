
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from Utility.Training_Utilities import *
from Utility.DelongTest import delong_roc_test
from lightgbm import LGBMClassifier
pd.options.mode.chained_assignment = None  # default='warn'

ImpMethod = 'TotalGain'

dpath = '../'
outfile = dpath + 'Results/Results_Pheno/s2.0_AccAUC_'+ImpMethod+'.csv'
data_df = pd.read_csv(dpath + 'Data/PredictorsData.csv')
my_f_lst = data_df.columns.tolist()[1:]
target_df = pd.read_csv(dpath + 'Data/target.csv')
field_dict_df = pd.read_csv(dpath + 'Data/FeatureDict.csv')
mydf = pd.merge(target_df, data_df, how = 'inner', on = ['eid'])

imp_f_df = pd.read_csv(dpath + 'Results/Results_Pheno/s1_Importance.csv')
imp_f_df.sort_values(by = ImpMethod + '_cv', ascending=False, inplace = True)
imp_f_lst = imp_f_df.Pro_code.tolist()[:30]

fold_id_lst = list(set(mydf.Region_code))

y_test_full = np.zeros(shape = [1,1])
for fold_id in fold_id_lst:
    test_idx = mydf['Region_code'].index[mydf['Region_code'] == fold_id]
    y_test_full = np.concatenate([y_test_full, np.expand_dims(mydf.iloc[test_idx].target_y, -1)])

y_pred_full_prev = y_test_full
tmp_f, AUC_cv_lst= [], []

for f in imp_f_lst:
    tmp_f.append(f)
    my_X = mydf[tmp_f]
    AUC_cv = []
    y_pred_full = np.zeros(shape = [1,1])
    for fold_id in fold_id_lst:
        train_idx = mydf['Region_code'].index[mydf['Region_code'] != fold_id]
        test_idx = mydf['Region_code'].index[mydf['Region_code'] == fold_id]
        X_train, X_test = mydf.iloc[train_idx][tmp_f], mydf.iloc[test_idx][tmp_f]
        y_train, y_test = mydf.iloc[train_idx].target_y, mydf.iloc[test_idx].target_y
        my_lgb = LGBMClassifier(objective='binary', metric='auc', is_unbalance=True,  n_jobs=4, verbosity=-1, seed=2020)
        my_lgb.set_params(**{'n_estimators': 500, 'max_depth': 15, 'num_leaves': 10,
                             'subsample': 0.7, 'learning_rate': 0.01, 'colsample_bytree': 0.7})
        my_lgb.fit(X_train, y_train)
        y_pred_prob = my_lgb.predict_proba(X_test)[:, 1]
        AUC_cv.append(np.round(roc_auc_score(y_test, y_pred_prob), 3))
        y_pred_full = np.concatenate([y_pred_full, np.expand_dims(y_pred_prob, -1)])
    log10_p = delong_roc_test(y_test_full[:,0], y_pred_full_prev[:,0], y_pred_full[:,0])
    y_pred_full_prev = y_pred_full
    tmp_out = np.array([np.round(np.mean(AUC_cv), 3), np.round(np.std(AUC_cv), 3), 10**log10_p[0][0]] + AUC_cv)
    AUC_cv_lst.append(tmp_out)
    print((f, np.mean(AUC_cv), 10**log10_p[0][0]))

AUC_df = pd.DataFrame(AUC_cv_lst, columns = ['AUC_mean', 'AUC_std', 'p_delong'] + ['AUC_' + str(i) for i in range(10)])

AUC_df = pd.concat((pd.DataFrame({'Pro_code':tmp_f}), AUC_df), axis = 1)

AUC_df['FieldID'] = [int(ele.split('-')[0]) for ele in AUC_df.Pro_code]
AUC_df = pd.merge(AUC_df, field_dict_df, how = 'left', on = ['FieldID'])


AUC_df.to_csv(outfile, index = False)

print('finished')



