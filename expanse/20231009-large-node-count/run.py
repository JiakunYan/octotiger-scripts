#!/usr/bin/env python

import os
import sys
import shutil
import copy
import json
sys.path.append("../../include")
from script_common import *

baseline = {
    "name": "lci",
    "nnodes_list": [64, 128],
    "max_level": 5,
    "griddim": 2,
    "stop_step": 30,
    "zc_threshold": 4096,
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
    "in_buffer_assembly": 1,
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 1,
    "ndevices": 2,
    "ncomps": 2
}


configs = [
    # # # LCI v.s. MPI
    # {**baseline, "name": "lci", "parcelport": "lci", "stop_step": 5},
    # {**baseline, "name": "mpi", "parcelport": "mpi", "sendimm": 0, "stop_step": 5},
    # {**baseline, "name": "mpi_i", "parcelport": "mpi", "sendimm": 1, "stop_step": 5},
    {**baseline, "name": "lci-grid8", "griddim": 8, "parcelport": "lci", "stop_step": 5},
    {**baseline, "name": "mpi-grid8", "griddim": 8, "parcelport": "mpi", "sendimm": 0, "stop_step": 5},
    {**baseline, "name": "mpi_i-grid8", "griddim": 8, "parcelport": "mpi", "sendimm": 1, "stop_step": 5},
    {**baseline, "name": "lci-grid8-l6", "griddim": 8, "max_level": 6, "parcelport": "lci", "stop_step": 5},
    {**baseline, "name": "mpi-grid8-l6", "griddim": 8, "max_level": 6, "parcelport": "mpi", "sendimm": 0, "stop_step": 5},
    {**baseline, "name": "mpi_i-grid8-l6", "griddim": 8, "max_level": 6, "parcelport": "mpi", "sendimm": 1, "stop_step": 5},
]
run_as_one_job = False

if __name__ == "__main__":
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    mkdir_s("./run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    if run_as_one_job:
        for config in configs:
            if len(config["nnodes_list"]) > 1:
                print("Cannot run as one job! Give up!")
                exit(1)

    for i in range(n):
        if run_as_one_job:
            for nnodes in configs[0]["nnodes_list"]:
                run_slurm(tag, nnodes, configs, name="all", time = "00:00:{}".format(len(configs) * 30))
        else:
            for config in configs:
                # print(config)
                for nnodes in config["nnodes_list"]:
                    if nnodes > 32:
                        run_slurm(tag, nnodes, config, time = "1:30", extra_args="--qos=unlim")
                    else:
                        run_slurm(tag, nnodes, config, time = "3:00")