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
    "zc_threshold": 4096,
    "task": "rs",
    "parcelport": "lci",
    "protocol": "putsendrecv",
    "comp_type": "queue",
    "progress_type": "rp",
    "prg_thread_num": "auto",
    "sendimm": 1,
    "backlog_queue": 0,
    "prepost_recv_num": 1,
    "zero_copy_recv": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 0,
    "ndevices": 2,
    "ncomps": 2
}

configs = [
    {**baseline, "nnodes_list": [2, 4, 8, 12, 16], "name": "mpi", "parcelport": "mpi", "sendimm": 0},
    {**baseline, "nnodes_list": [2, 4, 8, 12, 16], "name": "mpi_i", "parcelport": "mpi", "sendimm": 1},
    {**baseline, "nnodes_list": [2, 4, 8, 12, 16], "name": "lci", "parcelport": "lci"},
    # # Different Problem Size
    {**baseline, "name": "mpi-grid4", "parcelport": "mpi", "sendimm": 0, "griddim": 4},
    {**baseline, "name": "mpi-grid6", "parcelport": "mpi", "sendimm": 0, "griddim": 6},
    {**baseline, "name": "mpi-grid8", "parcelport": "mpi", "sendimm": 0, "griddim": 8},
    {**baseline, "name": "mpi_i-grid4", "parcelport": "mpi", "sendimm": 1, "griddim": 4},
    {**baseline, "name": "mpi_i-grid6", "parcelport": "mpi", "sendimm": 1, "griddim": 6},
    {**baseline, "name": "mpi_i-grid8", "parcelport": "mpi", "sendimm": 1, "griddim": 8},
    {**baseline, "name": "lci-grid4", "parcelport": "lci", "griddim": 4},
    {**baseline, "name": "lci-grid6", "parcelport": "lci", "griddim": 6},
    {**baseline, "name": "lci-grid8", "parcelport": "lci", "griddim": 8},
    # # sendimm
    {**baseline, "name": "lci_wo_i", "sendimm": 0},
    # # communication prototype + comp_type
    {**baseline, "name": "lci_sendrecv", "protocol": "sendrecv"},
    {**baseline, "name": "lci_sync", "comp_type": "sync"},
    # # ndevices + progress_type
    # {**baseline, "name": "lci_mt_d1", "ndevices": 1, "progress_type": "worker"},
    # {**baseline, "name": "lci_mt_d2", "ndevices": 2, "progress_type": "worker"},
    # {**baseline, "name": "lci_mt_d4", "ndevices": 4, "progress_type": "worker"},
    # {**baseline, "name": "lci_mt_d8", "ndevices": 8, "progress_type": "worker"},
    # {**baseline, "name": "lci_pin_d1", "ndevices": 1, "progress_type": "rp"},
    # {**baseline, "name": "lci_pin_d2", "ndevices": 2, "progress_type": "rp"},
    # {**baseline, "name": "lci_pin_d4", "ndevices": 4, "progress_type": "rp"},
    # {**baseline, "name": "lci_pin_d8", "ndevices": 8, "progress_type": "rp"},
    # # ncomps
    # {**baseline, "name": "lci_mt_d8_c2", "ndevices": 8, "progress_type": "worker", "ncomps": 2},
    # {**baseline, "name": "lci_mt_d8_c4", "ndevices": 8, "progress_type": "worker", "ncomps": 4},
    # {**baseline, "name": "lci_mt_d8_c8", "ndevices": 8, "progress_type": "worker", "ncomps": 8},
    # {**baseline, "name": "lci_pin_d8_c2", "ndevices": 8, "progress_type": "rp", "ncomps": 2},
    # {**baseline, "name": "lci_pin_d8_c4", "ndevices": 8, "progress_type": "rp", "ncomps": 4},
    # {**baseline, "name": "lci_pin_d8_c8", "ndevices": 8, "progress_type": "rp", "ncomps": 8},
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