import argparse
from ast import arg
import os
import pandas as pd
import numpy as np

def convert(args):
    dataset = args.dataset
    assert dataset in ["SST5", "TREC6", "TREC50"], "Invalid dataset type: %s!" % dataset

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=str, default="SST5")
    args = parser.parse_args()
    convert(args)
