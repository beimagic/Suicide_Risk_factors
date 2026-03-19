
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

region_fold_lst = [i for i in range(10)]

for region_fold in region_fold_lst:
    '''
    For regional cross validation, plot the sequential forward selection procedure
    Notably, we only plotted the top-30 features
    '''
    imp_df = pd.read_csv(dpath + 'Results/Suicide/TestingFold_' + str(region_fold) + '/s1_Importance.csv',
                         usecols=['Feature', 'Importance'])
    auc_df = pd.read_csv(dpath + 'Results/Suicide/TestingFold_' + str(region_fold) + '/s2.0_sf_selection.csv')
    mydf = pd.merge(imp_df, auc_df, how='left', on=['Feature'])
    mydf['AUC_lower'] = mydf['AUC_mean'] - 1.96 * mydf['AUC_std']
    mydf['AUC_upper'] = mydf['AUC_mean'] + 1.96 * mydf['AUC_std']
    mydf['f_idx'] = [i for i in range(1, len(mydf) + 1)]
    nb_f = get_nb_f(mydf)
    mydf = mydf.iloc[:30, :]
    fig, ax = plt.subplots(figsize=(20, 8))
    '''
    The plot include two y-axis, 
    left y-axis plot the feature importance scores
    right y-axis plot the incremental AUCs
    Notably, the importance scores and AUCs were previously derived based on each regional fold
    '''
    palette = sns.color_palette("Blues", n_colors=len(mydf))
    palette.reverse()
    sns.barplot(ax=ax, x='Feature', y="Importance", palette=palette,
                data=mydf.sort_values(by="Importance", ascending=False))
    y_imp_up_lim = round(mydf['Importance'].max() + 0.01, 2)
    ax.set_ylim([0, y_imp_up_lim])
    ax.tick_params(axis='y', labelsize=14)
    ax.set_xticklabels(mydf['FieldName'], rotation=45, fontsize=14, horizontalalignment='right', fontname='Helvetica')
    '''
    Color selected features in red font, and the number of features were determined based on sequential forward selection scheme
    '''
    my_col = ['r'] * nb_f + ['k'] * (len(mydf) - nb_f)
    for ticklabel, tickcolor in zip(plt.gca().get_xticklabels(), my_col):
        ticklabel.set_color(tickcolor)
    ax.set_ylabel('Predictor Importance', fontsize=18, fontname='Helvetica')
    ax.set_xlabel('')
    ax.grid(which='minor', alpha=0.2, linestyle=':')
    ax.grid(which='major', alpha=0.5, linestyle='--')
    ax.set_axisbelow(True)
    ax2 = ax.twinx()
    ax2.plot(np.arange(nb_f + 1), mydf['AUC_mean'][:nb_f + 1], 'red', alpha=0.8, marker='o')
    ax2.plot(np.arange(nb_f + 1, len(mydf)), mydf['AUC_mean'][nb_f + 1:], 'black', alpha=0.8, marker='o')
    ax2.plot([nb_f, nb_f + 1], mydf['AUC_mean'][nb_f:nb_f + 2], 'black', alpha=0.8, marker='o')
    plt.fill_between(mydf['f_idx'] - 1, mydf['AUC_lower'], mydf['AUC_upper'], color='tomato', alpha=0.2)
    ax2.set_ylabel('Cumulative AUC', fontsize=18, fontname='Helvetica')
    ax2.tick_params(axis='y', labelsize=14)
    y_auc_up_lim = round(mydf['AUC_upper'].max() + 0.02, 2)
    y_auc_low_lim = round(mydf['AUC_lower'].min() - 0.02, 2)
    ax2.set_ylim([y_auc_low_lim, y_auc_up_lim])
    fig.tight_layout()
    fig.tight_layout()
    plt.savefig(dpath + 'Results/Suicide/TestingFold_'+str(region_fold)+'/s2.1_sf_selection_plot.pdf', dpi = 300)
    plt.close()
    print(nb_f)

