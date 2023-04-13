import re
import glob
import numpy as np
import ast
import pandas as pd
import os,sys
sys.path.append("../../include")
from draw_simple import *

name = "20230330-first"
input_path = "run/slurm_output.*"
output_path = "data/"
edge_filename = {
    "format": "\S+slurm_output\.\S+-(\S+)-(\S+)-n(\S+)-l(\S+)\.(\S+)\.j\S+\.out",
    "label": ["job", "parcelport", "nnodes", "level", "tag"],
}
edge_data = {
    "format": "Total: (\S+)",
    # "format": "Computation: (\S+) \(\S+ %\)",
    "label": ["Time(s)"]
}
all_labels = edge_filename["label"] + edge_data["label"]

def get_typed_value(value):
    if value == '-nan':
        return np.nan
    try:
        typed_value = ast.literal_eval(value)
    except:
        typed_value = value
    return typed_value

if __name__ == "__main__":
    filenames = glob.glob(input_path)

    df = pd.DataFrame(columns=all_labels)
    state = "init"
    current_entry = dict()
    print("{} files in total".format(len(filenames)))
    for filename in filenames:
        found = False
        current_entry = dict()
        m = re.match(edge_filename["format"], filename)
        if m:
            current_data = [get_typed_value(x) for x in m.groups()]
            current_label = edge_filename["label"]
            for label, data in zip(current_label, current_data):
                current_entry[label] = data
        else:
            print("Ignore {}".format(filename))
            continue
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip()
                m = re.match(edge_data["format"], line)
                if m:
                    current_data = [get_typed_value(x) for x in m.groups()]
                    current_label = edge_data["label"]
                    for label, data in zip(current_label, current_data):
                        current_entry[label] = data
                    new_df = pd.DataFrame(current_entry, columns=all_labels, index=[1])
                    df = pd.concat([df, new_df], ignore_index=True)
                    found = True
                    break
        if not found:
            print("{} not found!".format(filename))
    df = df[all_labels]
    df = df.sort_values(by=all_labels)
    if df.shape[0] == 0:
        print("Error! Get 0 entries!")
        exit(1)
    else:
        print("get {} entries".format(df.shape[0]))
    df.to_csv(os.path.join(output_path, "{}.csv".format(name)))