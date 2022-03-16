#!/bin/bash
export TOKENIZERS_PARALLELISM=false
export DATA='data/sst-5/'
# export DATA='data/stanfordSentimentTreebank/'
python3 model/run.py --dataset_basedir $DATA \
                         --lr 2e-5  --max_epochs 10 \
                         --gpus 1 \
                         --concept_store $DATA/concept_store.pt \
                         --accelerator ddp \
                         --num_classes 5 \
                         --seed 22
