#!/bin/bash
export TOKENIZERS_PARALLELISM=false
export DATA_TYPE=6
python3 model/run.py --dataset_basedir data/trec/$DATA_TYPE/ \
                         --lr 2e-5  --max_epochs 50 \
                         --gpus 1 \
                         --concept_store data/trec/$DATA_TYPE/concept_store.pt \
                         --accelerator ddp \
                         --num_classes $DATA_TYPE
