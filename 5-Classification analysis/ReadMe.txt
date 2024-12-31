
ReadMe

Data:
  - PredictorsData.csv: UK Biobank phenotypic predictors used for analysis. It contains all 404 predictors after quality control.

  - TargetInfo.csv: UK Biobank target information and cross-validation IDs. Target was coded as column "target_y", cross-validation ID was coded as column of "region_cv_fold", and inner cv id was coded as "in_cv_fold".

  - FeatureDict.csv: Predictor dictionary of field IDs used in PredictorsData.csv.

  - target.csv: UK Biobank target information and cross-validation IDs used in our original analysis. The CV fold was named as "Region_code", which is exact the same as "region_cv_fold" in TargetInfo.csv.



Code:

  To run the code, please customize the working directory within each code file and ensure you have establish a Results folder named the same as ours. Please run the code following the sequence of files listed below. Notably, to ensure a strict 10-fold cross-validation, we recorded all statistics that each sub-folder 0-9 contain all results during each cv partition. For example, TestingFold_4 represents the results trained using region_cv_fold==0-3 & 5-9, and evaluated in region_cv_fold==4.
  
  Code of modeling contains a couple a sequential steps that strictly follows the descriptions from the manuscript as follows:
  
  Supplmentary Information:" The iterations stopped upon no observation of significant incremental on the model's performance of area under the ROC curve (AUC), determined as three consecutive insignificant DeLong statistics. The line chart demonstrated the sequential forward selection strategy that the model's performance climbed steeply when taking part in the first several predictors and gradually went flat with gentle fluctuation when additional ones came in.
  The machine-learning model was trained and evaluated through a 10-fold cross-validation by spatially partitioning the study cohort into ten folds based on the geographical locations of assessment centres (namely, East Midlands, London, North-East, North-West, Scotland, South-East, South-West, Wales, West Midlands, and Yorkshire and Humber). Specifically, within each iteration, the model was established using nine folds of data (training dataset) and was then deployed to the remaining fold (validation dataset), and such a scheme was repeated until all folds of data had been used as both training and validation datasets."

    - s1_ImpRanking.py: Calculate the information gain represents phenotype importance, corresponding to Results/Suicide/TestingFold_*/s1_Importance.csv.

    - s2.0_SFS.py: Sequential forward selection of phenotypes, corresponding to Results/Suicide/TestingFold_*/s2.0_sf_selection.csv.

    - s2.1_SFS_Plot.py: Visualization of the sequential selection, phenotypes was determined as three consecutive insignificant DeLong statistics, corresponding to Results/Suicide/TestingFold_*/s2.1_sf_selection_plot.pdf.

    - s3.0_pred_probs.py: Calculate the predicted probabilities based on phenotypes selected in step 2, corresponding to Results/Suicide/TestingFold_*/s3.0_pred_top*_features.csv.

    - s3.1_pred_probs-top10.py: Calculate the predicted probabilities based on top-10 ranked phenotypes in step 2, corresponding to Results/Suicide/TestingFold_*/s3.1_pred_top10_features.csv.

    - s4.0_Evaluation.py: Evaluate the predictions derived in step s3.0 within each fold and the take the average, ccorresponding to Results/Suicide/TestingFold_*/s4.0_evaluation_top*_features.csv.

    - s4.1_Evaluation-top10.py: Evaluate the predictions derived in step s3.1 within each fold and the take the average, ccorresponding to Results/Suicide/TestingFold_*/s4.1_evaluation_top10_features.csv.


  - Utility: supplementary functions for analysis

    - DelongTest.py: DeLong test

    - Training_Utilities.py: functions might be used within original code



Results:

  - Suicide/TestingFold_*: * represents 0 to 9, each folder contains the model strictly separted within 10 folders, models under each folder were trained and evaluated using an inner-cross-validation.

    - s1_Importance.csv: Phnotype importance based on all analyzed predictors, corresponding to Code/s1_ImpRanking.py

    - s2.0_sf_selection.csv: Sequential forward selection procedure of phenotypes based on s1_Importance.csv, corresponding to Code/s2.0_SFS.py

    - s2.1_sf_selection_plot.pdf: visualization of phenotype selections, corresponding to Code/s2.1_SFS_Plot.py.

    - s3.0_pred_top*_features.csv: Predicted probabilities based on selected phenotypes, corresponding to Code/s3.0_pred_probs.py.

    - s3.1_pred_top10_features.csv: Predicted probabilities based on top-10 selected phenotypes, corresponding to Code/s3.1_pred_probs-top10.py.

    - s4.0_evaluation_top*_features.csv: Evaluation of predicted probabilities calculated in s3.0_pred_top*_features.csv, corresponding to Code/s4_Evaluation.py.

    - s4.1_evaluation_top10_features.csv: Evaluation of predicted probabilities calculated in s3.1_pred_top10_features.csv, corresponding to Code/s4.1_Evaluation-top10.py.

  - RegionFold_evaluation_selected_features.csv: averaged evaluation metrics from 10 region cv folds based on s4.0_evaluation_top*_features.csv.
  
  - RegionFold_evaluation_top10_features.csv: averaged evaluation metrics from 10 region cv folds based on s4.1_evaluation_top10_features.csv.



Required environment to run the code
*.py file
Python 3.9.16

nunmpy == 1.23.5
pandas == 1.4.3
lightgbm == 3.3.2
sklearn == 1.2.2
tqdm == 4.64.0
joblib == 1.2.0
scipt==1.9.0

