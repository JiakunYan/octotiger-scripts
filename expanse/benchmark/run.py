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
    # baseline,
    # {**baseline, "name": "lci", "nnodes_list": [2]},
    {**baseline, "name": "lci", "nnodes_list": [2]},
    {**baseline, "name": "mpi", "nnodes_list": [2], "parcelport": "mpi", "sendimm": 0},
    {**baseline, "name": "mpi_sendimm", "nnodes_list": [2], "parcelport": "mpi", "sendimm": 1},
    # {**baseline, "name": "mpi", "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi_sendimm", "parcelport": "mpi", "sendimm": 1},
    # {**baseline, "name": "lci_sendrecv_sync_worker", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_sync_rp", "protocol": "sendrecv", "comp_type": "sync", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_queue_worker", "protocol": "sendrecv", "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_queue_rp", "protocol": "sendrecv", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_sync_worker", "comp_type": "sync", "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_sync_rp", "comp_type": "sync", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_queue_worker", "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_queue_rp", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_sync_worker_sendimm", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker"},
    # {**baseline, "name": "lci_sendrecv_sync_rp_sendimm", "protocol": "sendrecv", "comp_type": "sync"},
    # {**baseline, "name": "lci_sendrecv_queue_worker_sendimm", "protocol": "sendrecv", "progress_type": "worker"},
    # {**baseline, "name": "lci_sendrecv_queue_rp_sendimm", "protocol": "sendrecv"},
    # {**baseline, "name": "lci_putsendrecv_sync_worker_sendimm", "comp_type": "sync", "progress_type": "worker"},
    # {**baseline, "name": "lci_putsendrecv_sync_rp_sendimm", "comp_type": "sync"},
    # {**baseline, "name": "lci_putsendrecv_queue_worker_sendimm", "progress_type": "worker"},
    # {**baseline, "name": "lci_putsendrecv_queue_rp_sendimm"},
    # pthread
    # {**baseline, "name": "lci_sendrecv_sync_pthread", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "pthread", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_queue_pthread", "protocol": "sendrecv", "progress_type": "pthread", "sendimm": 0},
    # {**baseline, "name": "lci_sendrecv_sync_pthread_sendimm", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "pthread"},
    # {**baseline, "name": "lci_sendrecv_queue_pthread_sendimm", "protocol": "sendrecv", "progress_type": "pthread"},
    # {**baseline, "name": "lci_putsendrecv_sync_pthread", "comp_type": "sync", "progress_type": "pthread", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_sync_pthread_sendimm", "comp_type": "sync", "progress_type": "pthread"},
    # {**baseline, "name": "lci_putsendrecv_queue_pthread", "progress_type": "pthread", "sendimm": 0},
    # {**baseline, "name": "lci_putsendrecv_queue_pthread_sendimm", "progress_type": "pthread"},
    # putva
    # {**baseline, "name": "lci_putva_sync_worker", "protocol": "putva", "comp_type": "sync", "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_putva_sync_worker_sendimm", "protocol": "putva", "comp_type": "sync", "progress_type": "worker"},
    # {**baseline, "name": "lci_putva_queue_worker_sendimm", "protocol": "putva", "progress_type": "worker"},
    # {**baseline, "name": "lci_putva_queue_rp_sendimm", "protocol": "putva"},
    # backlog queue
    # {**baseline, "name": "lci_sendrecv_sync_worker_bq", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker", "sendimm": 0, "backlog_queue": 1},
    # {**baseline, "name": "lci_sendrecv_sync_worker_sendimm_bq", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker", "backlog_queue": 1},
    # {**baseline, "name": "lci_putsendrecv_queue_rp_sendimm_bq", "backlog_queue": 1},
    # 2 devices
    # {**baseline, "name": "lci_putva_queue_worker_sendimm_2dev", "progress_type": "worker", "use_two_device": 1},
    # {**baseline, "name": "lci_putva_queue_rp_sendimm_2dev", "use_two_device": 1},
    # prepost receives
    # {**baseline, "name": "lci_sendrecv_sync_worker_post8", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker", "sendimm": 0, "prepost_recv_num": 8},
    # {**baseline, "name": "lci_sendrecv_queue_worker_post8", "protocol": "sendrecv", "progress_type": "worker", "sendimm": 0, "prepost_recv_num": 8},
    # {**baseline, "name": "lci_sendrecv_sync_worker_sendimm_post8", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker", "prepost_recv_num": 8},
    # {**baseline, "name": "lci_sendrecv_queue_worker_sendimm_post8", "protocol": "sendrecv", "progress_type": "worker", "prepost_recv_num": 8},
    # No zero-copy receives
    # {**baseline, "name": "mpi_nozcr", "parcelport": "mpi", "sendimm": 0, "zero_copy_recv": 0},
    # {**baseline, "name": "lci_putsendrecv_queue_worker_sendimm_nozcr", "progress_type": "worker", "zero_copy_recv": 0},
    # Match table
    # {**baseline, "name": "lci_sendrecv_sync_worker_sendimm_hash", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker", "match_table_type": "hash"},
    # {**baseline, "name": "lci_putsendrecv_queue_worker_sendimm_hash", "progress_type": "worker", "match_table_type": "hash"},
    # {**baseline, "name": "lci_sendrecv_sync_worker_sendimm_mqueue", "protocol": "sendrecv", "comp_type": "sync", "progress_type": "worker", "match_table_type": "queue"},
    # {**baseline, "name": "lci_putsendrecv_queue_worker_sendimm_mqueue", "progress_type": "worker", "match_table_type": "queue"},
    # {**baseline, "name": "lci_sendrecv_sync_rp_sendimm_hash", "protocol": "sendrecv", "comp_type": "sync", "match_table_type": "hash"},
    # {**baseline, "name": "lci_putsendrecv_queue_rp_sendimm_hash", "match_table_type": "hash"},
    # {**baseline, "name": "lci_sendrecv_sync_rp_sendimm_mqueue", "protocol": "sendrecv", "comp_type": "sync", "match_table_type": "queue"},
    # {**baseline, "name": "lci_putsendrecv_queue_rp_sendimm_mqueue", "match_table_type": "queue"},
    # Others
    # {**baseline, "name": "lci_putva_sync_pthread", "protocol": "putva", "comp_type": "sync", "progress_type": "pthread", "sendimm": 0},
    # {**baseline, "name": "lci_putva_sync_rp", "protocol": "putva", "comp_type": "sync", "sendimm": 0},
    # {**baseline, "name": "lci_putva_sync_pthread_sendimm", "protocol": "putva", "comp_type": "sync", "progress_type": "pthread"},
    # {**baseline, "name": "lci_putva_sync_rp_sendimm", "protocol": "putva", "comp_type": "sync"},
    # {**baseline, "name": "lci_putva_queue_worker", "protocol": "putva", "progress_type": "worker", "sendimm": 0},
    # {**baseline, "name": "lci_putva_queue_pthread", "protocol": "putva", "progress_type": "pthread", "sendimm": 0},
    # {**baseline, "name": "lci_putva_queue_rp", "protocol": "putva", "sendimm": 0},
    # {**baseline, "name": "lci_putva_queue_pthread_sendimm", "protocol": "putva", "progress_type": "pthread"},

]

if __name__ == "__main__":
    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    mkdir_s("run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    for i in range(n):
        for config in configs:
            # print(config)
            for nnodes in config["nnodes_list"]:
                run_slurm(tag, nnodes, config, time="00:03:00")