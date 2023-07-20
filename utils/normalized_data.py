import json
import random
import numpy as np
class TruthfulQA:
    def __init__(self,path) -> None:
        with open(path) as f:
            self.data = json.load(f)
    def mc1_generator(self,n=-1):
        if n == -1:
            n = len(self.data)
        for i,item in enumerate(self.data[:n]):
            question = item["question"]
            options = list(item["mc1_targets"].keys()) 
            labels = list(item["mc1_targets"].values()) 
            idxes = [i for i in range(len(options))]
            random.shuffle(idxes)
            options_str = ""
            for j,idx in enumerate(idxes):
                options_str += chr(ord("A")+j) + ". " + options[idx] +"\n"
                if labels[idx] == 1:
                    ground_truth = j
            yield question, options_str, ground_truth

