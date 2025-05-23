#!/bin/bash
#PBS -N pda_numheads
#PBS -l select=1:ncpus=56:mem=372gb:ngpus=1:gpu_model=a100:phase=27,walltime=4:00:00
#PBS -q wficai
#PBS -j oe

echo "Running on host: "$HOSTNAME
echo "-------------------------------"
start=`date +%s`

# setup env
module load anaconda3/2022.10
module load cuda/11.7.0
source activate pda
cd /home/dane2/Code/pda_detection/code

# loop over number of heads
artifactfolder="/project/dane2/wficai/pda/model_run_artifacts/pda_cvtest/"
mkdir -p $artifactfolder
python train_pda_cv.py \
    configs/pda/pda_config.yaml \
    --artifact-folder ${artifactfolder} \
    --frame-csv "/project/dane2/wficai/pda/model_data/pda_train_val_test_remapped.csv" \
    --device 'cuda:0' \
    --pooling-method 'attn' \
    --num-heads 16 \
    --epochs 1 \
    2>&1 | tee ${artifactfolder}log.txt

end=`date +%s`
runtime=$((end-start))
echo "-------------------------------"
echo "Total runtime (s): "$runtime
echo "-------------------------------"
