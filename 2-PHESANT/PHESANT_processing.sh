#!/bin/bash
#SBATCH -J PHSANT
#SBATCH -p DCUq30
#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH -o %j.out
#SBATCH -e %j.err

module load R/4.2.0
# Initialize code
Dir="/home1/beizhang/Suicide/"
codeDir="${Dir}PHESANT-master/WAS/"

# define path
dataDir="${Dir}PHESANT-master/"
# results File
CatDir="${dataDir}results_1st_R/"
# expouse file and  trait of interests name
expFile="${dataDir}data_1st_R/data.csv"
trait_name="suicide"
## pheno data File
phenodataFile="${dataDir}phenotypes.csv"
# confounders
confFile="${dataDir}phenotypes_1st_R/cov.csv"
 
# ---Step1 Running a phenome scan in UK Biobank-----
# run PHESANT
Rscript phenomeScan.r \
--phenofile="$phenodataFile" \
--traitofinterestfile="$expFile" \
--variablelistfile="${dataDir}variable-lists/outcome-info.tsv" \
--datacodingfile="${dataDir}variable-lists/data-coding-ordinal-info.txt" \
--traitofinterest="$trait_name" \
--resDir="${CatDir}results/"  \
--userId="userId"  \
--sensitivity \
--genetic=TRUE \
--confounderfile="$confFile"

# ---Step 2 Post-processing of results----
Rscript mainCombineResults.r \
--resDir="${CatDir}results/"  \
--variablelistfile="${dataDir}variable-lists/outcome-info.tsv"