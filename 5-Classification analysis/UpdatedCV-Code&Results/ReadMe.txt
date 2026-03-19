
ReadMe

1. Overview

This repository contains the full code and results for the sensitivity analyses of the machine-learning models in the manuscript: “Identifying Behaviour-related and Physiological Risk Factors for Suicide Attempts in the UK Biobank”.
These analyses were conducted to strictly enforce fold-specific feature selection within a 10-fold cross-validation framework, with feature ranking and model training performed independently in each training fold. The purpose of these sensitivity analyses is to evaluate the robustness of both model performance and feature rankings under more conservative methodological assumptions.


2. Code Execution

  To run the code, please customize the working directory within each code file and ensure you have establish a Results folder named the same as ours. Please run the code following the sequence of files listed below. Notably, to ensure a strict 10-fold cross-validation, we recorded all statistics that each sub-folder 0-9 contain all results during each cv partition. For example, TestingFold_4 represents the results trained using region_cv_fold==0-3 & 5-9, and evaluated in region_cv_fold==4.
  
  Code of modeling contains a couple a sequential steps that strictly follows the descriptions from the manuscript as follows:
  
  Supplmentary Information:"The iterations stopped upon no observation of significant incremental on the model's performance of area under the ROC curve (AUC), determined as three consecutive insignificant DeLong statistics. The line chart demonstrated the sequential forward selection strategy that the model's performance climbed steeply when taking part in the first several predictors and gradually went flat with gentle fluctuation when additional ones came in.
  The machine-learning model was trained and evaluated through a 10-fold cross-validation by spatially partitioning the study cohort into ten folds based on the geographical locations of assessment centres (namely, East Midlands, London, North-East, North-West, Scotland, South-East, South-West, Wales, West Midlands, and Yorkshire and Humber). Specifically, within each iteration, the model was established using nine folds of data (training dataset) and was then deployed to the remaining fold (validation dataset), and such a scheme was repeated until all folds of data had been used as both training and validation datasets."

    - s1_ImpRanking.py: Calculate the information gain represents phenotype importance, corresponding to ../Results/Suicide/TestingFold_*/s1_Importance.csv.

    - s2.0_SFS.py: Sequential forward selection of phenotypes, corresponding to ../Results/Suicide/TestingFold_*/s2.0_sf_selection.csv.

    - s2.1_SFS_Plot.py: Visualization of the sequential selection, phenotypes was determined as three consecutive insignificant DeLong statistics, corresponding to ../Results/Suicide/TestingFold_*/s2.1_sf_selection_plot.pdf.

    - s2.2_Importance_plot.py: Visualization of the averaged importance across ten folds, corresponding to ../Results/Suicide/s2.2_Importance_cross_folds.csv and ../Results/Suicide/s2.2_Importance_cross_folds_plot.pdf.

    - s3.0_pred_probs.py: Train models based on phenotypes selected in step 2 and calculate the predicted risks, corresponding to ../Results/Suicide/TestingFold_*/s3.0_top*_features_trained_model.pkl and ../Results/Suicide/TestingFold_*/s3.0_top*_features_predicted_risks.csv.

    - s3.1_pred_probs-top10.py: Train models based on top-10 ranked phenotypes in step 2 and calculate the predicted risks, corresponding to ../Results/Suicide/TestingFold_*/s3.1_top10_features_trained_model.pkl and ../Results/Suicide/TestingFold_*/s3.1_top10_features_predicted_risks.csv.

    - s4.0_Evaluation.py: Evaluate the predictions derived in step s3.0 within each fold and the take the average, ccorresponding to ../Results/Suicide/TestingFold_*/s4.0_evaluation_top*_features.csv.

    - s4.1_Evaluation-top10.py: Evaluate the predictions derived in step s3.1 within each fold and the take the average, ccorresponding to ../Results/Suicide/TestingFold_*/s4.1_evaluation_top10_features.csv.


  - Utility: supplementary functions for analysis

    - DelongTest.py: DeLong test

    - Training_Utilities.py: functions might be used within original code



3. Results Structure
  - Suicide/TestingFold_*: * represents 0 to 9, each folder contains the model strictly separted within 10 folders, models under each folder were trained and evaluated using an inner-cross-validation.

    - s1_Importance.csv: Phnotype importance based on all analyzed predictors, corresponding to Code/s1_ImpRanking.py

    - s2.0_sf_selection.csv: Sequential forward selection procedure of phenotypes based on s1_Importance.csv, corresponding to Code/s2.0_SFS.py

    - s2.1_sf_selection_plot.pdf: visualization of phenotype selections, corresponding to Code/s2.1_SFS_Plot.py.

    - s3.0_top*_features_trained_model.pkl: Trained models based on selected phenotypes, corresponding to Code/s3.0_pred_probs.py.

    - s3.0_top*_features_predicted_risks.csv: Predicted probabilities based on selected phenotypes, corresponding to Code/s3.0_pred_probs.py.

    - s3.1_top10_features_trained_model.pkl: Trained models based on top-10 selected phenotypes, corresponding to Code/s3.1_pred_probs-top10.py.

    - s3.1_top10_features_predicted_risks.csv: Predicted probabilities based on top-10 selected phenotypes, corresponding to Code/s3.1_pred_probs-top10.py.

    - s4.0_evaluation_top*_features.csv: Evaluation of predicted probabilities calculated in s3.0_pred_top*_features.csv, corresponding to Code/s4_Evaluation.py.

    - s4.1_evaluation_top10_features.csv: Evaluation of predicted probabilities calculated in s3.1_pred_top10_features.csv, corresponding to Code/s4.1_Evaluation-top10.py.

  - s2.2_Importance_cross_folds.csv: averaged importance derived from importance scores from each fold, corresponding to Code/s2.2_Importance_plot.py.

  - s2.2_Importance_cross_folds_plot.pdf: plot the averaged importance derived from importance scores from each fold, notably top phenotypes were colored in red, which was determined based on the average number of selected features, corresponding to Code/s2.2_Importance_plot.py.

  - RegionFold_evaluation_selected_features.csv: averaged evaluation metrics from 10 region cv folds based on s4.0_evaluation_top*_features.csv.
  
  - RegionFold_evaluation_top10_features.csv: averaged evaluation metrics from 10 region cv folds based on s4.1_evaluation_top10_features.csv.



4. Required environment
Python version: Python 3.9.16
Required packages:
numpy == 1.23.5
pandas == 1.4.3
lightgbm == 3.3.2
sklearn == 1.2.2
tqdm == 4.64.0
joblib == 1.2.0
scipt==1.9.0

