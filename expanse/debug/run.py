#!/usr/bin/env python

import os
import sys
import shutil
import copy
import json
sys.path.append("../../include")
from script_common import *

baseline = {
    "name": "mpi",
    "nnodes_list": [32],
    "max_level": 6,
    "griddim": 8,
    "zc_threshold": 8192,
    "task": "rs",
    "parcelport": "mpi",
    "protocol": "sendrecv",
    "comp_type": "sync",
    "progress_type": "worker",
    "sendimm": 0,
    "backlog_queue": 0,
    "use_two_device": 0,
    "prg_thread_core": -1,
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
            run_slurm(tag, nnodes, config, time = "2:00")