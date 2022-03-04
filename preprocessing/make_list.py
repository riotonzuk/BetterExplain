import json
from argparse import ArgumentParser

def convert_to_list(filename):
    with open(filename) as f:
        result = []
        for line in f.readlines():
            result.append(eval(line))
        json.dump(result, open(filename, "w"))

if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("--filename")
    opt = argparser.parse_args()
    convert_to_list(opt.filename)
