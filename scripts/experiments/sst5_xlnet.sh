#!/bin/bash
export TOKENIZERS_PARALLELISM=false
python3 model/run.py --dataset_basedir data/stanfordSentimentTreebank/ \
                         --lr 2e-5  --max_epochs 1 \
                         --gpus 1 \
                         --concept_store data/stanfordSentimentTreebank/concept_store.pt \
                         --accelerator ddp \
                         --num_classes 5 \
