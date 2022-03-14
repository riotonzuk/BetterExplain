import argparse
from ast import arg
import os
import pandas as pd
import numpy as np
from torchnlp.datasets import trec_dataset

def convert(args):
    dataset = args.dataset
    assert dataset in ["SST5", "TREC6", "TREC50", "SUBJ"], "Invalid dataset type: %s!" % dataset

    if dataset == "SST5":
        def get_label(lbl):
            for i in range(1, 6):
                if lbl <= i * 0.2:
                    return i-1
            return 4

        path = "data/stanfordSentimentTreebank"
        sentences = os.path.join(path, "datasetSentences.txt")
        labels = os.path.join(path, "sentiment_labels.txt")
        splits = os.path.join(path, "datasetSplit.txt")

        with open(sentences,"r") as f:
            data = f.readlines()[1:]
        print(data[0])
        with open(labels, "r") as f:
            lbl = f.readlines()[1:]

        train_sentences = []
        train_labels = []
        dev_sentences = []
        dev_labels = []
        test_sentences = []
        test_labels = []

        with open(splits, "r") as f:
            # 1=train, 2=dev, 3=test
            for i, tup in enumerate(f.readlines()):
                if i == 0:
                    # ignore column headers
                    continue
                # print(tup)
                sid, assign = tup.split(",")
                sid, assign = int(sid) - 1, int(assign)

                dat = data[sid].split("\t")[-1].replace("\n", "")
                lb = get_label(float(lbl[sid].split("|")[-1]))

                if assign == 1:
                    train_sentences.append(dat)
                    train_labels.append(lb)
                elif assign == 2:
                    dev_sentences.append(dat)
                    dev_labels.append(lb)
                elif assign == 3:
                    test_sentences.append(dat)
                    test_labels.append(lb)

        train_df = pd.DataFrame({
            "sentence":np.array(train_sentences),
            "label":np.array(train_labels)                
        })
        dev_df = pd.DataFrame({
            "sentence":np.array(dev_sentences),
            "label":np.array(dev_labels)                
        })
        test_df = pd.DataFrame({
            "sentence":np.array(test_sentences),
            "label":np.array(test_labels)                
        })

        train_df.to_csv(os.path.join(path, "train.tsv"), sep="\t", index=False)
        dev_df.to_csv(os.path.join(path,"dev.tsv"), sep="\t", index=False)
        test_df.to_csv(os.path.join(path,"test.tsv"), sep="\t", index=False)
    elif dataset in ("TREC6", "TREC50"):
        classes = int(dataset[4:])
        path = os.path.join("data", dataset)
        is_TREC50 = classes == 50
        train_data = trec_dataset(path, train=True, fine_grained=is_TREC50)
        counter = 0
        label_map = {}

        for sample in train_data:
            label = sample["label"]
            if label not in label_map:
                label_map[label] = counter
                counter += 1

        test_data = trec_dataset(".", test=True, fine_grained=is_TREC50)
        train_split = 9 * len(train_data) // 10
        train_data, dev_data = train_data[:train_split], train_data[train_split:]

        sets = [(f"train", train_data), \
                (f"dev", dev_data), \
                (f"test", test_data)]

        for save_filename, data in sets:
            save_path = os.path.join(f"{path}", f"{save_filename}.tsv")
            with open(save_path, "w") as output_file:
                output_file.write(f"sentence\tlabel\n")
                for sample in data:
                    data = sample["text"]
                    label = label_map[sample["label"]]
                    output_file.write(f"{data}\t{label}\n")
    elif dataset == "SUBJ":
        path = "data/SUBJ"
        os.makedirs(path, exist_ok=True)
        data_dir = "data/movie-review"
        # quote: subjective, plot: objective
        with open(os.path.join(data_dir, "quote.tok.gt9.5000"), "r", encoding = "ISO-8859-1") as quote:
            subj = quote.readlines()[1:]
            # for i, line in enumerate(subj):
            #     subj[i] = line[1:-1]
        with open(os.path.join(data_dir, "plot.tok.gt9.5000"), "r", encoding = "ISO-8859-1") as plot:
            obj = plot.readlines()[1:]
            # for i, line in enumerate(obj):
            #     obj[i] = line[1:-1]
        # for each class
        # train: first 4000 samples
        # dev: next 500 samples
        # test: next 500 samples
        splits = {
            "train": (0,4000),
            "dev": (4000,4500),
            "test": (4500,5000),
        }
        # subjective: label 0, objective, label 1
        for name, (start, end) in splits.items():
            subj_data = subj[start:end]
            obj_data = obj[start:end]
            dat = subj_data + obj_data
            labels = [0] * len(subj_data) + [1] * len(obj_data)
            df = pd.DataFrame({
                # "sentence":np.array(dat),
                # "label":np.array(labels)
                "sentence": pd.Series(dat, dtype="string"),
                "label":pd.Series(labels, dtype="int")
            })
            df.to_csv(os.path.join(path, f"{name}.tsv"), sep="\t", index=False)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=str, default="SST5")
    args = parser.parse_args()
    convert(args)
