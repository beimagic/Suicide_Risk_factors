
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from Utility.DelongTest import delong_roc_test
from lightgbm import LGBMClassifier
from tqdm import tqdm
pd.options.mode.chained_assignment = None  # default='warn'

dpath = '/Volumes/JasonWork/Projects/OtherProjects/ZhangBei/'
data_df = pd.read_csv(dpath + 'Data/PredictorsData.csv')
my_f_lst = data_df.columns.tolist()[1:]
target_df = pd.read_csv(dpath + 'Data/TargetInfo.csv')
field_dict_df = pd.read_csv(dpath + 'Data/FeatureDict.csv', usecols = ['FieldID', 'FieldName'])
mydf = pd.merge(target_df, data_df, how = 'inner', on = ['eid'])

region_fold_lst = list(set(mydf.region_cv_fold))
inner_cv_fold_lst = list(set(mydf.in_cv_fold))

for region_fold in tqdm(region_fold_lst):
    imp_f_df = pd.read_csv(dpath + 'Results/Suicide/TestingFold_' + str(region_fold) + '/s1_Importance.csv')
    imp_f_lst = imp_f_df.Feature.tolist()[:30]
    traindf = mydf.loc[mydf.region_cv_fold != region_fold]
    traindf.reset_index(inplace = True, drop = True)
    cv_AUC_lst, tmp_f = [], []
    y_test_full, y_pred_full_prev = np.zeros(shape=[1, 1]), np.zeros(shape=[1, 1])
    for inner_cv_fold_id in inner_cv_fold_lst:
        in_test_idx = traindf['in_cv_fold'].index[traindf['in_cv_fold'] == inner_cv_fold_id]
        y_test_full = np.concatenate([y_test_full, np.expand_dims(traindf.iloc[in_test_idx].target_y, -1)])
    y_pred_full_prev = y_test_full
    for f in tqdm(imp_f_lst):
        tmp_f.append(f)
        my_X = mydf[tmp_f]
        in_cv_AUC_lst = []
        y_pred_full = np.zeros(shape=[1, 1])
        for inner_cv_fold_id in inner_cv_fold_lst:
            in_train_idx = traindf['in_cv_fold'].index[traindf['in_cv_fold'] != inner_cv_fold_id]
            in_test_idx = traindf['in_cv_fold'].index[traindf['in_cv_fold'] == inner_cv_fold_id]
            in_cv_X_train, in_cv_X_test = traindf.iloc[in_train_idx][tmp_f], traindf.iloc[in_test_idx][tmp_f]
            in_cv_y_train, in_cv_y_test = traindf.iloc[in_train_idx].target_y, traindf.iloc[in_test_idx].target_y
            my_lgb = LGBMClassifier(objective='binary', metric='auc', is_unbalance=True, verbosity=-1, seed=2020)
            my_lgb.set_params(**{'n_estimators': 500, 'max_depth': 15, 'num_leaves': 10,
                                 'subsample': 0.7, 'learning_rate': 0.01, 'colsample_bytree': 0.7})
            my_lgb.fit(in_cv_X_train, in_cv_y_train)
            in_cv_y_pred = my_lgb.predict_proba(in_cv_X_test)[:, 1]
            in_cv_AUC_lst.append(np.round(roc_auc_score(in_cv_y_test, in_cv_y_pred), 3))
            y_pred_full = np.concatenate([y_pred_full, np.expand_dims(in_cv_y_pred, -1)])
        log10_p = delong_roc_test(y_test_full[:, 0], y_pred_full_prev[:, 0], y_pred_full[:, 0])
        y_pred_full_prev = y_pred_full
        in_cv_out = np.array([np.round(np.mean(in_cv_AUC_lst), 3), np.round(np.std(in_cv_AUC_lst), 3), 10 ** log10_p[0][0]] + in_cv_AUC_lst)
        cv_AUC_lst.append(in_cv_out)
        print((f, np.mean(in_cv_AUC_lst), 10 ** log10_p[0][0]))
    cv_AUC_df = pd.DataFrame(cv_AUC_lst, columns=['AUC_mean', 'AUC_std', 'p_delong'] + ['inner_cv_AUC_' + str(i) for i in range(10)])
    cv_AUC_df = pd.concat((pd.DataFrame({'Feature': tmp_f}), cv_AUC_df), axis=1)
    cv_AUC_df['FieldID'] = [int(ele.split('-')[0]) for ele in cv_AUC_df.Feature]
    cv_AUC_df = pd.merge(cv_AUC_df, field_dict_df, how='left', on=['FieldID'])
    cv_AUC_df.to_csv(dpath + 'Results/Suicide/TestingFold_'+str(region_fold)+'/s2.0_sf_selection.csv', index=False)

print('finished')



