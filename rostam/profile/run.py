#!/usr/bin/env python3

import os
import sys
import shutil
import copy
import json
sys.path.append(f'{os.environ["HOME"]}/workspace/octotiger-scripts/include')
from script_common import *

baseline = {
    "name": "lci",
    "nnodes_list": [8],
    "max_level": 5,
    "griddim": 2,
    "stop_step": 30,
    "zc_threshold": 8192,
    "task": "rs",
    "parcelport": "lci",
    "protocol": "putsendrecv",
    "comp_type": "queue",
    "progress_type": "worker",
    "prg_thread_num": "auto",
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 0,
    "ndevices": 4,
    "ncomps": 4
}

configs = [
    # baseline,
    {**baseline, "name": "lci_c1", "ncomps": 1},
    {**baseline, "name": "lci_c2", "ncomps": 2},
    {**baseline, "name": "lci_c4", "ncomps": 4},
    # {**baseline, "name": "lci_l5_worker_d1", "ndevices": 1, "progress_type": "worker"},
    # {**baseline, "name": "lci_l5_worker_d2", "ndevices": 2, "progress_type": "worker"},
    # {**baseline, "name": "lci_l5_worker_d4", "ndevices": 4, "progress_type": "worker"},
    # {**baseline, "name": "lci_l5_rp_d1", "ndevices": 1, "progress_type": "rp"},
    # {**baseline, "name": "lci_l5_rp_d2", "ndevices": 2, "progress_type": "rp"},
    # {**baseline, "name": "lci_l5_rp_d4", "ndevices": 4, "progress_type": "rp"},
    # {**baseline, "name": "lci_l5_rp1_d1", "ndevices": 1, "progress_type": "rp", "prg_thread_num": "1"},
    # {**baseline, "name": "lci_l5_rp1_d2", "ndevices": 2, "progress_type": "rp", "prg_thread_num": "1"},
    # {**baseline, "name": "lci_l5_rp1_d4", "ndevices": 4, "progress_type": "rp", "prg_thread_num": "1"},
]

if __name__ == "__main__":
    mkdir_s("./run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    for config in configs:
        # print(config)
        for nnodes in config["nnodes_list"]:
            run_slurm(tag, nnodes, config)