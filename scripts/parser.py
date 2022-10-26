#!/usr/bin/env python

## parse a source file and extract ingredients and instructions.

import re
import json
import os
import sys
import jaconv
import Mykytea
from html.parser import HTMLParser
from tokenizers import normalizers


class KurashiruParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.found = False
        self.title = ""
        self.ingredients = []
        self.instructions = []

    def handle_starttag(
        self,
        tag,
        attrs,
    ):
        #print("Encountered a start tag {} ({})".format(tag, type(tag)))
        pass

    def handle_endtag(
        self,
        tag,
    ):
        #print("Encountered an end tag {} ({})".format(tag, type(tag)))
        pass

    def handle_data(
        self,
        data,
    ):
        if "detail-content" in data:

            assert not self.found
            self.found = True

            #x = json.loads(data)
            x = json.loads(data[data.find("ssrContext = ") + 13:][:-2]) # remove ";\n"
            x = x["state"]["fetchVideo"]["data"]["data"]["attributes"]

            self.title = x["title"]

            heads = {}
            for d in x["ingredients"]:
                if d["type"] == "heading":
                    heads[d["id"]] = d["title"]

            self.ingredients = []
            for d in x["ingredients"]:

                if "group-id" in d.keys() and d["group-id"] is not None:
                    head = "({})".format(heads[d["group-id"]])
                else:
                    head = ""

                if d["type"] == "ingredients":

                    ingr = d["name"] if head == "" else head + " " + d["name"]
                    self.ingredients += [ingr + " " + d["quantity-amount"].replace("\r\n", "")]

            self.instructions = [
                "{}.".format(d["sort-order"]) + d["body"].replace("\r\n", "")
                if d["sort-order"] != 0 else "準備." + d["body"].replace("\r\n", "")
                for d in x["instructions"]
            ]
            

if __name__ == "__main__":
    normalizer = normalizers.Sequence([normalizers.NFKC()])
    kytea = kytea = Mykytea.Mykytea("-notags -model jp-0.4.7-1.mod")
    data_dir = sys.argv[1]

    for recipe_id in os.listdir(data_dir):
        recipe_dir = "{}/{}".format(data_dir, recipe_id)
        text = open("{}/source.txt".format(recipe_dir)).read()

        parser = KurashiruParser()
        parser.feed(text)
        assert parser.found

        with open("{}/title.txt".format(recipe_dir), "w") as fw:
            fw.write(parser.title + "\n")
    
        with open("{}/ingredients.txt".format(recipe_dir), "w") as fw1, \
             open("{}/ingredients.tok".format(recipe_dir), "w") as fw2:

            for line in parser.ingredients:
                line = normalizer.normalize_str(line).replace("　", "")
                line = jaconv.h2z(line, digit=True, ascii=True)

                fw1.write(line + "\n")
                fw2.write(" ".join([w for w in kytea.getWS(line)]).replace("　 ", "") + "\n")

        with open("{}/instructions.txt".format(recipe_dir), "w") as fw1, \
             open("{}/instructions.tok".format(recipe_dir), "w") as fw2:

            for line in parser.instructions:
                line = normalizer.normalize_str(line).replace("　", "")
                line = jaconv.h2z(line, digit=True, ascii=True)

                fw1.write(line + "\n")
                fw2.write(" ".join([w for w in kytea.getWS(line)]).replace("　 ", "") + "\n")
    

