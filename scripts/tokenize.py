#!/usr/bin/env python

import os
import json
import argparse

data_dir = "./data/recipes"
ann_path = "./data/annotations.json"

annotations = json.load(open(ann_path))

for recipe_id in os.listdir(data_dir):
    ann = annotations[recipe_id]
    recipe_dir = os.path.join(data_dir, recipe_id)

    ## tokenize words
    for file_type in ("ingredient", "instruction"):
        with open(os.path.join(recipe_dir, "{}s.tok".format(file_type)), "w") as fw:
            for i, line in enumerate(open(os.path.join(recipe_dir, "{}s.txt".format(file_type))).readlines()):
                sentence = line.rstrip()

                tokenized = [
                    sentence[w["start_char"]: w["end_char"]]
                    for w in ann["{}s".format(file_type)][i]
                ]

                fw.write(" ".join(tokenized) + "\n")


