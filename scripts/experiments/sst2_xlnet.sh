#!/bin/bash
export TOKENIZERS_PARALLELISM=false
python3 model/run.py --dataset_basedir data/SST-2/ \
                         --lr 2e-5  --max_epochs 50 \
                         --gpus 1 \
                         --concept_store data/SST-2/concept_store.pt \
                         --accelerator ddp \
