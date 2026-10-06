
import numpy as np
import pandas as pd

dpath = '../'
tmp_result_file = 'RegionFold_evaluation_selected_features'
#tmp_result_file = 'RegionFold_evaluation_top10_features'

res_df = pd.read_csv(dpath + 'Results/Suicide/'+tmp_result_file+'.csv')

'''
Extract meaningful metrics, rename columns and save results
'''

res_df1 = res_df[['Cutoff', 'AUC', 'Prec', 'Sens', 'Acc', 'Spec', 'F1', 'Youden']]
res_df1.rename(columns = {'Prec':'Precision', 'Sens':'Recall', 'Acc':'Accuracy', 'Spec':'Specificity'}, inplace = True)
res_df1.index = ['TestingFold_'+str(i) for i in range(10)] + ['MEAN', 'SD', 'Output']
res_df1.index.name = 'Evaluation fold'
res_df1.to_csv(dpath + 'Results/Suicide/'+tmp_result_file+'_final.csv', index = True)

print('Done')

