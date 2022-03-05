# BetterExplain
CSE 517 (NLP) project 

## Package Requirements
We took the setup script from the original
implementation(https://github.com/dheerajrajagopal/SelfExplain).  To setup the
packages we recommend using a conda envrionment. E.g. after conda is installed
and setup(https://www.anaconda.com/),
```
conda create -n selfexplain python=3.8 -y
conda activate selfexplain
```
Above will activate the envionment.

Packages can be installed via
```
pip install -r requirements.txt
```

For pytorch please refer to https://pytorch.org/get-started/locally/

## Preprocessing

Data for preprocessing available in `data/` folder

On a python shell, do the following for installing the parser

```python
>>> import benepar
>>> benepar.download('benepar_en3')
```

To get all datasets in the same `train/dev/test.tsv` format, run
```shell
python preprocessing/get_tsv.py <SST5/...>
```

```shell
# sh scripts/run_preprocessing.sh
# SST2 XLNET
sh scripts/preprocessing/sst2_xlnet.sh
# SST5 XLNET
sh scripts/preprocessing/sst5_xlnet.sh
```


## Training

```shell
# SE_XLNet
sh scripts/experiments/sst2_xlnet.sh
sh scripts/experiments/sst5_xlnet.sh
```
