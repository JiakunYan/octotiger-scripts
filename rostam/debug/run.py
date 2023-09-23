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
    "nnodes_list": [2],
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
    "ncomps": 2,
}

configs = [
    baseline,
    # {**baseline, "name": "lci_c1", "ncomps": 1},
    # {**baseline, "name": "lci_c2", "ncomps": 2},
    # {**baseline, "name": "lci_c4", "ncomps": 4},
    # {**baseline, "name": "lci_l5_worker_d1", "ndevices": 1, "progress_type": "worker"},
    # {**baseline, "name": "lci_l5_worker_d2", "ndevices": 2, "progress_type": "worker"},
    # {**baseline, "name": "lci_l5_worker_d4", "ndevices": 4, "progress_type": "worker"},
    # {**baseline, "name": "lci_l5_rp_d1", "ndevices": 1, "progress_type": "rp"},
    # {**baseline, "name": "lci_l5_rp_d2", "ndevices": 2, "progress_type": "rp"},
    # {**baseline, "name": "lci_l5_rp_d4", "ndevices": 4, "progress_type": "rp"},
    # {**baseline, "name": "lci_l5_rp1_d1", "ndevices": 1, "progress_type": "rp", "prg_thread_num": "1"},
    # {**baseline, "name": "lci_l5_rp1_d2", "ndevices": 2, "progress_type": "rp", "prg_thread_num": "1"},
    # {**baseline, "name": "lci_l5_rp1_d4", "ndevices": 4, "progress_type": "rp", "prg_thread_num": "1"},
    # {**baseline, "name": "lci_d8", "ndevices": 8},
    # {**baseline, "name": "mpi_l5", "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi_i_l5", "parcelport": "mpi", "sendimm": 1},
    # {**baseline, "name": "lci_l6", "max_level": 6},
    # {**baseline, "name": "mpi_l6", "parcelport": "mpi", "max_level": 6},
    # {**baseline, "name": "mpi_i_l6", "parcelport": "mpi", "sendimm": 1, "max_level": 6},
    # {**baseline, "name": "lci_putsendrecv_queue_rp", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_sync_worker_sendimm", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker"},
    # {**baseline, "name": "lci_sendrecv_sync_rp_sendimm", "protocol": "sendrecv", "comp_type": "sync"},
    # {**baseline, "name": "lci_sendrecv_queue_worker_sendimm", "protocol": "sendrecv", "progress_type": "worker"},
    # {**baseline, "name": "lci_sendrecv_queue_rp_sendimm", "protocol": "sendrecv"},
    # {**baseline, "name": "lci_putsendrecv_sync_worker_sendimm", "comp_type": "sync", "progress_type": "worker"},
    # {**baseline, "name": "lci_putsendrecv_sync_rp_sendimm", "comp_type": "sync"},
    # {**baseline, "name": "lci_putsendrecv_queue_worker_sendimm", "progress_type": "worker"},
    # {**baseline, "name": "lci_putsendrecv_queue_rp_sendimm", "progress_type": "rp"},
    # {**baseline, "name": "lci_putsendrecv_queue_rp_sendimm_1prg", "progress_type": "rp", "prg_thread_num": "1"},
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
                run_slurm(tag, nnodes, config, time = "5:00")