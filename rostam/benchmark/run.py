#!/usr/bin/env python3

import os
import sys
import shutil
import copy
import json
sys.path.append("../../include")
from script_common import *

baseline = {
    "name": "lci",
    "nnodes_list": [8],
    "max_level": 5,
    "griddim": 8,
    "zc_threshold": 8192,
    "task": "rs",
    "parcelport": "lci",
    "protocol": "putsendrecv",
    "comp_type": "queue",
    "progress_type": "rp",
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 0
}

configs = [
    # {**baseline, "name": "lci", "nnodes_list": [2, 4, 8, 15, 16], "parcelport": "lci"},
    # {**baseline, "name": "mpi", "nnodes_list": [2, 4, 8, 15, 16], "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi_i", "nnodes_list": [2, 4, 8, 15, 16], "parcelport": "mpi", "sendimm": 1},
    {**baseline, "name": "lci_psr_cq_pin", "nnodes_list": [15], "sendimm": 0},
    {**baseline, "name": "lci_sr_sy_mt_i", "nnodes_list": [15], "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker"},
    {**baseline, "name": "lci_sr_sy_pin_i", "nnodes_list": [15], "protocol": "sendrecv", "comp_type": "sync"},
    {**baseline, "name": "lci_sr_cq_mt_i", "nnodes_list": [15], "protocol": "sendrecv", "progress_type": "worker"},
    {**baseline, "name": "lci_sr_cq_pin_i", "nnodes_list": [15], "protocol": "sendrecv"},
    {**baseline, "name": "lci_psr_sy_mt_i", "nnodes_list": [15], "comp_type": "sync", "progress_type": "worker"},
    {**baseline, "name": "lci_psr_sy_pin_i", "nnodes_list": [15], "comp_type": "sync"},
    {**baseline, "name": "lci_psr_cq_mt_i", "nnodes_list": [15], "progress_type": "worker"},
    {**baseline, "name": "lci_psr_cq_pin_i", "nnodes_list": [15]},
]

if __name__ == "__main__":
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    mkdir_s("./run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    for i in range(n):
        for config in configs:
            # print(config)
            for nnodes in config["nnodes_list"]:
                run_slurm(tag, nnodes, config, time = "3:00")