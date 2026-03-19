
ReadMe

1. Overview

This repository contains the complete code and corresponding results for the machine-learning analyses reported in the manuscript: “Identifying Behaviour-related and Physiological Risk Factors for Suicide Attempts in the UK Biobank”. 

2. Feature Inclusion and Ranking Strategy

The Machine-learning models in this study were trained using the complete set of behaviour-related features, without any pre-selection based on whole-sample association analyses. Feature importance rankings used in the main analyses were derived from the full dataset. This design choice was made to obtain a stable and interpretable set of predictors, and to reduce variability introduced by fluctuating feature rankings across individual cross-validation folds.

To explicitly address potential concerns regarding data leakage or performance inflation, we additionally conducted strict fold-specific cross-validation analyses, in which feature ranking and selection were performed independently within each training fold. The corresponding code and results are provided in the UpdatedCV-Code&Results folder. These sensitivity analyses demonstrate that both the selected top features and overall model performance were highly consistent with those obtained using full-dataset feature rankings, supporting the robustness of the reported findings.


3. Code Execution

To run the code, please customize the working directory within each script and ensure that a Results folder is created with the same structure as provided in this repository.

Please execute the scripts in the following order:

    - s1_ImpRanking.py: Calculate the information gain represents phenotype importance, corresponding to OriginalCode&Results/Results/Results_Pheno/s1_Importance.csv.

    - s2.0_SFS.py: Sequential forward selection of phenotypes, corresponding to OriginalCode&Results/Results/Results_Pheno/s2.0_AccAUC_TotalGain.csv.

    - s2.1_SFS_Plot.py: Visualization of the sequential selection, phenotypes was determined as three consecutive insignificant DeLong statistics, corresponding to OriginalCode&Results/Results/Results_Pheno/s2.1_AccAUC_TotalGain.pdf.

    - s3_Prediction.py: Train models and calculate the predicted probabilities based on phenotypes selected in previous step, corresponding to OriginalCode&Results/Results/Results_Pheno/s3_PredProbs.csv and OriginalCode&Results/Results/Results_Pheno/s3.0_trained_models/cv_*_trained_model.pkl.

    - s4_Evaluation.py: Evaluate the predictions within each fold and the take the average, ccorresponding to OriginalCode&Results/Results/Results_Pheno/s4_Evaluations.csv.


  - Utility: supplementary functions for analysis

    - DelongTest.py: DeLong test

    - Training_Utilities.py: functions might be used within original code



4. Results Structure

  - Results_Pheno:

    - s1_Importance.csv: CSF protein importance based on adjusted significant proteins in s00_Associations, corresponding to OriginalCode&Results/Code/s1_ImpRanking.py

    - s2.0_AccAUC_TotalGain.csv: Sequential forward selection procedure of phenotypes based on s1_Importance.csv, corresponding to OriginalCode&Results/Code/s2.0_SFS.py

    - s2.1_AccAUC_TotalGain.pdf: visualization of phenotype selections, corresponding to OriginalCode&Results/Code/s2.1_SFS_Plot.py.

    - s3.0_trained_models
        - cv_*_trained_model.pkl: Trained models based on pre-selected phenotypes, corresponding to Code/s3_Prediction.py.

    - s3_PredProbs.csv: Predicted probabilities based on selected phenotypes , corresponding to OriginalCode&Results/Code/s3_Prediction.py.

    - s4_Evaluations.csv: Evaluation of predicted probabilities calculated in s3_pred_top*_features.csv, corresponding to OriginalCode&Results/Code/s4_Evaluation.py.



5. Required environment to run the code
Python version: Python 3.9.16

Required packages:
nunmpy == 1.23.5
pandas == 1.4.3
lightgbm == 3.3.2
sklearn == 1.2.2
tqdm == 4.64.0
joblib == 1.2.0
scipt==1.9.0

