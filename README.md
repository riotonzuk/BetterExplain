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

## Preprocessing (Currently Only for SST-2)

Data for preprocessing available in `data/` folder

On a python shell, do the following for installing the parser

```python
>>> import benepar
>>> benepar.download('benepar_en3')
```

```shell
sh scripts/run_preprocessing.sh
```


## Training (Currently Only for SST-2)

```shell
sh scripts/run_self_explain.sh
```
