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
    "nnodes_list": [32],
    "max_level": 6,
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
    "reg_mem": 1
}

configs = [
    {**baseline, "name": "lci", "nnodes_list": [2, 4, 8, 16, 32]},
    {**baseline, "name": "mpi", "nnodes_list": [2, 4, 8, 16, 32], "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi_sendimm", "nnodes_list": [32], "parcelport": "mpi", "sendimm": 1},
]
run_as_one_job = False

if __name__ == "__main__":
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    mkdir_s("./run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    for i in range(n):
        if run_as_one_job:
            for nnodes in configs[0]["nnodes_list"]:
                run_slurm(tag, nnodes, configs, name="all", time = "3:00")
        else:
            for config in configs:
                # print(config)
                for nnodes in config["nnodes_list"]:
                    run_slurm(tag, nnodes, config, time = "3:00")