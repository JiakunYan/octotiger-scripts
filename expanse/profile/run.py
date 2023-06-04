#!/usr/bin/env python

import os
import sys
import shutil
import copy
import json
sys.path.append(f'{os.environ["HOME"]}/workspace/octotiger-scripts/include')
from script_common import *

baseline = {
    "name": "lci",
    "nnodes_list": [32],
    "griddim": 8,
    "zc_threshold": 8192,
    "task": "rs",
    "parcelport": "lci",
    "max_level": 6,
    "protocol": "sendrecv",
    "comp_type": "queue",
    "progress_type": "worker",
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
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