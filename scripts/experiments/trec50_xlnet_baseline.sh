#!/bin/bash
export TOKENIZERS_PARALLELISM=false
python3 model/run.py --dataset_basedir data/TREC50/ \
                         --lr 2e-5  --max_epochs 10 \
                         --gpus 1 \
                         --concept_store data/TREC50/concept_store.pt \
                         --accelerator ddp \
                         --num_classes 50 \
                         --seed 22 \
                         --baseline
