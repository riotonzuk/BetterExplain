#!/bin/bash
export TOKENIZERS_PARALLELISM=false
python3 model/run.py --dataset_basedir data/SUBJ/ \
                         --lr 2e-5  --max_epochs 10 \
                         --gpus 1 \
                         --concept_store data/SUBJ/concept_store.pt \
                         --accelerator ddp \
                         --seed 18
