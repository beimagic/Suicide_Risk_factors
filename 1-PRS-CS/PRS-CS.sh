#!/bin/bash
#SBATCH -J PRS
#SBATCH -p DCUq30
#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH -o %j.out
#SBATCH -e %j.err

# calculate posterior effect size
module load miniconda3/base
pip3 install scipy h5py
for i in $(seq 1 22)
do
python3 $PRScsx  \
--ref_dir="${LD_ref_dir}" \
--bim_prefix="${target_path}ukb_imp_chr${i}" \
--sst_file="${basedata_path}EUR_noUKB_QC.txt"  \
--n_gwas=477979 \
--pop=EUR \
--chrom=$i \
--out_dir="${out_path}" \
--out_name=PRS_effect_chr
done

# weight effct size
for i in $(seq 1 22)
do
plink2 \
--bfile ${target_path}ukb_imp_chr${i} \
--score ${out_path}/PRS_effect_chr${i}.txt 2 4 6 ignore-dup-ids list-variants cols=+scoresums \
--out  ${out_path}/prs_chr${i}
done

