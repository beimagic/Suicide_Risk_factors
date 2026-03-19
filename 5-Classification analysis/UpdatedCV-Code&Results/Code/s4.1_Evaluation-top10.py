import os.path
import numpy as np
from scipy import interp
from sklearn.metrics import roc_curve
import pandas as pd
from sklearn.metrics import brier_score_loss, average_precision_score
from sklearn.metrics import roc_auc_score, confusion_matrix
import glob

def threshold(array, cutoff):
    '''
    :param array: list of predicted risks
    :param cutoff: pre-determined cutoff based on fuction Find_Optimal_Cutoff
    :return: threshold arrays that classified 0 if predicted risk < threshold o.w. 1
    '''
    array1 = array.copy()
    array1[array1 < cutoff] = 0
    array1[array1 >= cutoff] = 1
    return array1

def Find_Optimal_Cutoff(mydf, target_col, pred_col):
    '''
    :param mydf: dataframe with target y and predicted risks
    :param target_col: column name of target y
    :param pred_col: column name of predicted risks
    :return: optimized cutoff value that maximize the Youden Index
    '''
    fpr, tpr, threshold = roc_curve(mydf[target_col], mydf[pred_col])
    i = np.arange(len(tpr))
    roc = pd.DataFrame({'tf': pd.Series(tpr - (1 - fpr), index=i), 'threshold': pd.Series(threshold, index=i)})
    roc_t = roc.iloc[(roc.tf - 0).abs().argsort()[:1]]
    return list(roc_t['threshold'])

def get_eval(y_test, pred_prob, cutoff):
    '''
    :param y_test: ground truth
    :param pred_prob: predicted risks
    :param cutoff: optimized cutoff value
    :return: evaluation arrays of metrics
    '''
    pred_binary = threshold(pred_prob, cutoff)
    tn, fp, fn, tp = confusion_matrix(y_test, pred_binary).ravel()
    acc = (tp + tn) / (tp + tn + fp + fn)
    sens = tp / (tp + fn)
    spec = tn / (tn + fp)
    prec = tp / (tp + fp)
    Youden = sens + spec - 1
    f1 = 2 * prec * sens / (prec + sens)
    auc = roc_auc_score(y_test, pred_prob)
    apr = average_precision_score(y_test, pred_prob)
    brier = brier_score_loss(y_test, pred_prob)
    nnd = 1 / Youden
    evaluations = np.round((cutoff, acc, sens, spec, prec, Youden, f1, auc, apr, nnd, brier), 4)
    evaluations = pd.DataFrame(evaluations).T
    evaluations.columns = ['Cutoff', 'Acc', 'Sens', 'Spec', 'Prec', 'Youden', 'F1', 'AUC', 'APR', 'NND', 'BRIER']
    evaluations = evaluations[['Cutoff', 'Acc', 'Sens', 'Spec', 'Prec', 'Youden', 'F1', 'AUC', 'APR', 'NND', 'BRIER']]
    return evaluations

def get_cv_output(mydf, y_true_col, y_pred_col, fold_col, fold_id_lst, cutoff):
    '''
    :param mydf: data frame contains the following columns
    :param y_true_col: column name of ground truth
    :param y_pred_col: column name of predicted risks
    :param fold_col: column name of regional fold data partition
    :param fold_id_lst: regional fold ids, here is 0-9
    :param cutoff: optimized cutoff value
    :return: evaluation arrays of metrics that averaged cross all regional folds
    '''
    result_df = pd.DataFrame()
    for fold_id in fold_id_lst:
        tmp_idx = mydf[fold_col].index[mydf[fold_col] == fold_id]
        tmpdf = mydf.iloc[tmp_idx]
        tmpdf.reset_index(inplace = True, drop = True)
        y_test, pred_prob = tmpdf[y_true_col], tmpdf[y_pred_col]
        tmp_result_df = get_eval(y_test, pred_prob, cutoff)
        result_df = pd.concat([result_df, tmp_result_df], axis = 0)
    result_df = result_df.T
    result_df['MEAN'] = result_df.mean(axis=1)
    result_df['STD'] = result_df.std(axis=1)
    output_lst = []
    for i in range(11):
        my_mean = str(np.round(result_df['MEAN'][i], 3))
        my_std = str(np.round(result_df['STD'][i], 3))
        output_lst.append(my_mean + ' +- ' + my_std)
    result_df['output'] = output_lst
    return result_df.T

dpath = '../'
outputfile = dpath + 'Results/Suicide/TestingFold_'+str(iter)+'/s6_eval.csv'
'''
region_fold_lst: 0-9, indicating the region of participants' visiting center
inner_cv_fold_lst: 0-9, ten folds of inner cross-validation within each regional fold, which was pre-assigned
'''
region_fold_lst = [i for i in range(10)]
inner_cv_fold_lst = [i for i in range(10)]
cv_results_lst = []

for region_fold in region_fold_lst:
    '''
    For regional cross validation, read the predicted risks
    get optimized cutoff value and calculate the evaluation metrics across inner fold cross validation
    '''
    mydf = pd.read_csv(glob.glob(dpath + 'Results/Suicide/TestingFold_'+str(region_fold)+'/s3.1_top*.csv')[0])
    opt_ct = Find_Optimal_Cutoff(mydf, 'target_y', 'y_pred_probs')[0]
    fold_id_lst = [i for i in range(10)]
    results = get_cv_output(mydf, 'target_y', 'y_pred_probs', 'in_cv_fold', inner_cv_fold_lst, opt_ct)
    results.index = ['inner_cv_iter' + str(fold) for fold in fold_id_lst] + ['Mean', 'StandarDeviation', 'Output']
    results.to_csv(dpath + 'Results/Suicide/TestingFold_'+str(region_fold)+'/s4.1_evaluation_top10_features.csv', index = True)
    cv_results_lst.append(results.iloc[10,:].tolist())

'''
Combine evaluation metrics derived from each regional CV to calculate the overall results
'''
cv_results_df = pd.DataFrame(cv_results_lst)
cv_results_df = cv_results_df.T
cv_results_df['MEAN'] = cv_results_df.mean(axis=1)
cv_results_df['STD'] = cv_results_df.std(axis=1)
output_lst = []
for i in range(11):
    my_mean = str(np.round(cv_results_df['MEAN'][i], 3))
    my_std = str(np.round(cv_results_df['STD'][i], 3))
    output_lst.append(my_mean + ' +- ' + my_std)
cv_results_df['output'] = output_lst
cv_results_df = cv_results_df.T
cv_results_df.columns = ['Cutoff', 'Acc', 'Sens', 'Spec', 'Prec', 'Youden', 'F1', 'AUC', 'APR', 'NND', 'BRIER']
cv_results_df.to_csv(dpath + 'Results/Suicide/RegionFold_evaluation_top10_features.csv')

print('Done')

