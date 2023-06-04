import json
import re
import glob
import numpy as np
import ast
import pandas as pd
import os,sys
sys.path.append("../../include")
from draw_simple import *

name = "20230601-all"
input_path = "run/slurm_output.*"
output_path = "data/"
filename_pattern = {
    "format": "\S+\.n(\d+)-(\S+)\.j\S+",
    "label": ["nnodes", "name"],
}

line_patterns = [
{
    "format": "Config: (.+)",
    "label": ["config"],
},
{
    "format": "Total: (\S+)",
    "label": ["Total(s)"]
},
{
    "format": "Computation: (\S+) \(\S+ %\)",
    "label": ["Computation(s)"]
},
{
    "format": "^Regrid: (\S+) \(\S+ %\)",
    "label": ["Regrid(s)"]
}]
all_labels = [y for x in line_patterns for y in x["label"]]

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

    df = None
    state = "init"
    current_entry = dict()
    print("{} files in total".format(len(filenames)))
    for filename in filenames:
        current_entry = dict()
        m = re.match(filename_pattern["format"], filename)
        if m:
            current_data = [get_typed_value(x) for x in m.groups()]
            current_label = filename_pattern["label"]
            for label, data in zip(current_label, current_data):
                current_entry[label] = data
        else:
            print("Ignore {}".format(filename))
            continue

        matched_count = 0
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip()
                for pattern in line_patterns:
                    m = re.match(pattern["format"], line)
                    if m:
                        current_data = [get_typed_value(x) for x in m.groups()]
                        current_label = pattern["label"]
                        for label, data in zip(current_label, current_data):
                            if label == "config":
                                data.pop("nnodes_list")
                                current_entry.update(data)
                            else:
                                current_entry[label] = data
                        matched_count += 1
                        break

        if matched_count != len(line_patterns):
            print("{} not found!".format(filename))
        else:
            print(current_entry)
            new_df = pd.DataFrame(current_entry, columns=list(current_entry.keys()), index=[1])
            if df is None:
                df = new_df
            else:
                df = pd.concat([df, new_df], ignore_index=True)

    # df = df[all_labels]
    # df = df.sort_values(by=all_labels)
    # Sort dataframe
    name_ordering = [
        # baseline,
        "mpi",
        "lci",
        "mpi_sendimm",
        "lci_sendrecv_sync_worker",
        "lci_sendrecv_sync_rp",
        "lci_sendrecv_queue_worker",
        "lci_sendrecv_queue_rp",
        "lci_putsendrecv_sync_worker",
        "lci_putsendrecv_sync_rp",
        "lci_putsendrecv_queue_worker",
        "lci_putsendrecv_queue_rp",
        "lci_sendrecv_sync_worker_sendimm",
        "lci_sendrecv_sync_rp_sendimm",
        "lci_sendrecv_queue_worker_sendimm",
        "lci_sendrecv_queue_rp_sendimm",
        "lci_putsendrecv_sync_worker_sendimm",
        "lci_putsendrecv_sync_rp_sendimm",
        "lci_putsendrecv_queue_worker_sendimm",
        "lci_putsendrecv_queue_rp_sendimm",
        # pthread
        # "lci_sendrecv_sync_pthread",
        # "lci_sendrecv_queue_pthread",
        # "lci_sendrecv_sync_pthread_sendimm",
        # "lci_sendrecv_queue_pthread_sendimm",
        # "lci_putsendrecv_sync_pthread",
        # "lci_putsendrecv_sync_pthread_sendimm",
        # "lci_putsendrecv_queue_pthread",
        # "lci_putsendrecv_queue_pthread_sendimm",
        # # putva
        # "lci_putva_sync_worker",
        # "lci_putva_sync_worker_sendimm",
        # "lci_putva_queue_worker_sendimm",
        # "lci_putva_queue_rp_sendimm",
        # # backlog queue
        # "lci_sendrecv_sync_worker_bq",
        # "lci_sendrecv_sync_worker_sendimm_bq",
        # "lci_putsendrecv_queue_rp_sendimm_bq",
        # # 2 devices
        # "lci_putva_queue_worker_sendimm_2dev",
        # "lci_putva_queue_rp_sendimm_2dev",
        # # prepost receives
        # "lci_sendrecv_sync_worker_post8",
        # "lci_sendrecv_queue_worker_post8",
        # "lci_sendrecv_sync_worker_sendimm_post8",
        # "lci_sendrecv_queue_worker_sendimm_post8",
        # # No zero-copy receives
        # "mpi_nozcr",
        # "lci_putsendrecv_queue_rp_sendimm_nozcr",
        # # Match table
        # "lci_sendrecv_sync_worker_sendimm_hash",
        # "lci_putsendrecv_queue_worker_sendimm_hash",
        # "lci_sendrecv_sync_worker_sendimm_mqueue",
        # "lci_putsendrecv_queue_worker_sendimm_mqueue",
        # "lci_sendrecv_sync_rp_sendimm_hash",
        # "lci_putsendrecv_queue_rp_sendimm_hash",
        # "lci_sendrecv_sync_rp_sendimm_mqueue",
        # "lci_putsendrecv_queue_rp_sendimm_mqueue",
        # # Others
        # "lci_putva_sync_pthread",
        # "lci_putva_sync_rp",
        # "lci_putva_sync_pthread_sendimm",
        # "lci_putva_sync_rp_sendimm",
        # "lci_putva_queue_worker",
        # "lci_putva_queue_pthread",
        # "lci_putva_queue_rp",
        # "lci_putva_queue_pthread_sendimm",
    ]
    df["name"] = pd.Categorical(df["name"], name_ordering)
    df = df.sort_values("name")

    if df.shape[0] == 0:
        print("Error! Get 0 entries!")
        exit(1)
    else:
        print("get {} entries".format(df.shape[0]))
    df.to_csv(os.path.join(output_path, "{}.csv".format(name)))