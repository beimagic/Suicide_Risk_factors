
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.mode.chained_assignment = None  # default='warn'

def get_nb_f(mydf):
    '''
    Calculate the stopping point
    Stopped upon no improvement over three consecutive features with DeLong p-values<0.05
    '''
    p_lst = mydf.p_delong.tolist()
    i = 0
    while((p_lst[i]<0.05)|(p_lst[i+1]<0.05)|(p_lst[i+2]<0.05)):
        i+=1
    return i

dpath = '../'

data_df = pd.read_csv(dpath + 'Data/PredictorsData.csv', nrows = 1)
field_dict_df = pd.read_csv(dpath + 'Data/FeatureDict.csv', usecols = ['FieldID', 'FieldName'])
my_f_df = pd.DataFrame({'Feature':data_df.columns.tolist()[1:]})
my_f_df['FieldID'] = [int(ele.split('-')[0]) for ele in my_f_df.Feature]
imp_df = pd.merge(my_f_df, field_dict_df, how='left', on=['FieldID'])

region_fold_lst = [i for i in range(10)]
nb_f_lst = []

for region_fold in region_fold_lst:
    '''
    Concatenate the importance score across all regional folds
    Save the number of features selected across all regional folds
    '''
    imp_df_fold = pd.read_csv(dpath + 'Results/Suicide/TestingFold_' + str(region_fold) + '/s1_Importance.csv',
                         usecols=['Feature', 'Importance'])
    imp_df_fold.columns = ['Feature', 'Importance_cv'+str(region_fold)]
    imp_df = pd.merge(imp_df, imp_df_fold, how='left', on = 'Feature')
    auc_df_fold = pd.read_csv(dpath + 'Results/Suicide/TestingFold_' + str(region_fold) + '/s2.0_sf_selection.csv')
    nb_f_lst.append(get_nb_f(auc_df_fold))

'''
Calculate the averaged importance score across all regional folds
'''
imp_df['Importance_cv'] = imp_df[['Importance_cv'+str(region_fold) for region_fold in region_fold_lst]].mean(axis=1)
imp_df['Importance_std'] = imp_df[['Importance_cv'+str(region_fold) for region_fold in region_fold_lst]].std(axis=1)
imp_df.sort_values(by='Importance_cv', ascending=False, inplace=True)
imp_df.to_csv(dpath + 'Results/Suicide/s2.2_Importance_cross_folds.csv', index=False)

'''
Calculate the averaged number of features selected across all regional folds
'''
nb_f = int(np.mean(nb_f_lst))
imp_df = imp_df.iloc[:30,:]
fig, ax = plt.subplots(figsize=(20, 8))
'''
Plot the averaged importance scores across all regional folds
Color the top-selected features based on the average number of features
'''
palette = sns.color_palette("Blues", n_colors=30)
palette.reverse()
sns.barplot(ax=ax, x='Feature', y="Importance_cv", palette=palette, data=imp_df.sort_values(by="Importance_cv", ascending=False))
y_imp_up_lim = round(imp_df['Importance_cv'].max() + 0.01, 2)
ax.set_ylim([0, y_imp_up_lim])
ax.tick_params(axis='y', labelsize=14)
ax.set_xticklabels(imp_df['FieldName'], rotation=45, fontsize=14, horizontalalignment='right', fontname='Helvetica')
my_col = ['r'] * nb_f + ['k'] * (len(imp_df) - nb_f)
for ticklabel, tickcolor in zip(plt.gca().get_xticklabels(), my_col):
    ticklabel.set_color(tickcolor)
ax.set_ylabel('Predictor Importance', fontsize=18, fontname='Helvetica')
ax.set_xlabel('')
ax.grid(which='minor', alpha=0.2, linestyle=':')
ax.grid(which='major', alpha=0.5, linestyle='--')
ax.set_axisbelow(True)
fig.tight_layout()
fig.tight_layout()
plt.savefig(dpath + 'Results/Suicide/s2.2_Importance_cross_folds_plot.pdf', dpi=300)
plt.close()

