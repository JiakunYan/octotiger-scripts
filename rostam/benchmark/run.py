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
    "nnodes_list": [16],
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
    "ndevices": 2,
    "ncomps": 1
}

configs = [
    # {**baseline, "name": "lci", "nnodes_list": [2, 4, 8, 16], "parcelport": "lci"},
    # {**baseline, "name": "mpi", "nnodes_list": [2, 4, 8, 16], "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi_i", "nnodes_list": [2, 4, 8, 16], "parcelport": "mpi", "sendimm": 1},
    # {**baseline, "name": "lci_wo_i", "nnodes_list": [2, 4, 8, 16], "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv", "nnodes_list": [2, 4, 8, 16], "protocol": "sendrecv"},
    # {**baseline, "name": "lci_sync", "nnodes_list": [2, 4, 8, 16], "comp_type": "sync"},
    # {**baseline, "name": "lci_worker_d1", "nnodes_list": [2, 4, 8, 16], "ndevices": 1, "progress_type": "worker"},
    # # {**baseline, "name": "lci_worker_d2", "nnodes_list": [2, 4, 8, 16], "ndevices": 2, "progress_type": "worker"},
    # {**baseline, "name": "lci_worker_d4", "nnodes_list": [2, 4, 8, 16], "ndevices": 4, "progress_type": "worker"},
    # {**baseline, "name": "lci_rp_d1", "nnodes_list": [2, 4, 8, 16], "ndevices": 1, "progress_type": "rp"},
    # {**baseline, "name": "lci_rp_d2", "nnodes_list": [2, 4, 8, 16], "ndevices": 2, "progress_type": "rp"},
    # {**baseline, "name": "lci_rp_d4", "nnodes_list": [2, 4, 8, 16], "ndevices": 4, "progress_type": "rp"},
    # Different Problem Size
    {**baseline, "name": "mpi-grid4", "nnodes_list": [8], "parcelport": "mpi", "sendimm": 0, "griddim": 4},
    {**baseline, "name": "mpi-grid6", "nnodes_list": [8], "parcelport": "mpi", "sendimm": 0, "griddim": 6},
    {**baseline, "name": "mpi-grid8", "nnodes_list": [8], "parcelport": "mpi", "sendimm": 0, "griddim": 8},
    {**baseline, "name": "mpi_i-grid4", "nnodes_list": [8], "parcelport": "mpi", "sendimm": 1, "griddim": 4},
    {**baseline, "name": "mpi_i-grid6", "nnodes_list": [8], "parcelport": "mpi", "sendimm": 1, "griddim": 6},
    {**baseline, "name": "mpi_i-grid8", "nnodes_list": [8], "parcelport": "mpi", "sendimm": 1, "griddim": 8},
    {**baseline, "name": "lci-grid4", "nnodes_list": [8], "parcelport": "lci", "griddim": 4},
    {**baseline, "name": "lci-grid6", "nnodes_list": [8], "parcelport": "lci", "griddim": 6},
    {**baseline, "name": "lci-grid8", "nnodes_list": [8], "parcelport": "lci", "griddim": 8},
    {**baseline, "name": "lci_rp-grid4", "nnodes_list": [8], "parcelport": "lci", "griddim": 4, "progress_type": "rp"},
    {**baseline, "name": "lci_rp-grid6", "nnodes_list": [8], "parcelport": "lci", "griddim": 6, "progress_type": "rp"},
    {**baseline, "name": "lci_rp-grid8", "nnodes_list": [8], "parcelport": "lci", "griddim": 8, "progress_type": "rp"},
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