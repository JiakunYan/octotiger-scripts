#!/usr/bin/env python

import os
import sys
import shutil
import copy
import json
sys.path.append(f'{os.environ["HOME"]}/workspace/octotiger-scripts/include')
from script_common import *

baseline = {
    "name": "mpi-i",
    "nnodes_list": [32],
    "griddim": 8,
    "zc_threshold": 8192,
    "task": "rs",
    "parcelport": "mpi",
    "max_level": 5,
    "protocol": "putsendrecv",
    "comp_type": "queue",
    "progress_type": "rp",
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_cas"
}

configs = [
    baseline,
]

if __name__ == "__main__":
    mkdir_s("./run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    for config in configs:
        # print(config)
        for nnodes in config["nnodes_list"]:
            run_slurm(tag, nnodes, config)