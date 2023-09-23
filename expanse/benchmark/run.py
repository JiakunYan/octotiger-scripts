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
    "match_table_type": "hashqueue",
    "cq_type": "array_atomic_faa",
    "reg_mem": 1,
    "ndevices": 2,
    "ncomps": 2
}


configs = [
    # LCI v.s. MPI
    {**baseline, "nnodes_list": [2, 4, 8, 16, 32], "name": "mpi", "parcelport": "mpi", "sendimm": 0},
    {**baseline, "nnodes_list": [2, 4, 8, 16, 32], "name": "mpi_i", "parcelport": "mpi", "sendimm": 1},
    {**baseline, "nnodes_list": [2, 4, 8, 16, 32], "name": "lci", "parcelport": "lci"},
    # Different Problem Size
    {**baseline, "name": "mpi-grid4", "parcelport": "mpi", "sendimm": 0, "griddim": 4},
    {**baseline, "name": "mpi-grid6", "parcelport": "mpi", "sendimm": 0, "griddim": 6},
    {**baseline, "name": "mpi-grid8", "parcelport": "mpi", "sendimm": 0, "griddim": 8},
    {**baseline, "name": "mpi_i-grid4", "parcelport": "mpi", "sendimm": 1, "griddim": 4},
    {**baseline, "name": "mpi_i-grid6", "parcelport": "mpi", "sendimm": 1, "griddim": 6},
    # {**baseline, "name": "mpi_i-grid8", "parcelport": "mpi", "sendimm": 1, "griddim": 8},
    {**baseline, "name": "lci-grid4", "parcelport": "lci", "griddim": 4},
    {**baseline, "name": "lci-grid6", "parcelport": "lci", "griddim": 6},
    {**baseline, "name": "lci-grid8", "parcelport": "lci", "griddim": 8},
    # communication prototype + comp_type
    {**baseline, "name": "lci_sendrecv", "protocol": "sendrecv"},
    {**baseline, "name": "lci_sync", "comp_type": "sync"},
    # ndevices + progress_type
    {**baseline, "name": "lci_mt_d1_c1", "ndevices": 1, "progress_type": "worker", "ncomps": 1},
    {**baseline, "name": "lci_mt_d2_c1", "ndevices": 2, "progress_type": "worker", "ncomps": 1},
    {**baseline, "name": "lci_mt_d4_c1", "ndevices": 4, "progress_type": "worker", "ncomps": 1},
    {**baseline, "name": "lci_pin_d1_c1", "ndevices": 1, "progress_type": "rp", "ncomps": 1},
    {**baseline, "name": "lci_pin_d2_c1", "ndevices": 2, "progress_type": "rp", "ncomps": 1},
    {**baseline, "name": "lci_pin_d4_c1", "ndevices": 4, "progress_type": "rp", "ncomps": 1},
    # ncomps
    {**baseline, "name": "lci_mt_d4_c2", "ndevices": 4, "progress_type": "worker", "ncomps": 2},
    {**baseline, "name": "lci_mt_d4_c4", "ndevices": 4, "progress_type": "worker", "ncomps": 4},
    {**baseline, "name": "lci_pin_d4_c2", "ndevices": 4, "progress_type": "rp", "ncomps": 2},
    {**baseline, "name": "lci_pin_d4_c4", "ndevices": 4, "progress_type": "rp", "ncomps": 4},
    # Upper-layer
    {**baseline, "name": "lci_wo_i", "sendimm": 0},
    {**baseline, "name": "lci_alock", "special_branch": "ipdps_nohack1"},
    {**baseline, "name": "lci_tlock", "special_branch": "ipdps_nohack2"},
    {**baseline, "name": "lci_atlock", "special_branch": "ipdps_nohack12"},
    {**baseline, "name": "lci_agas_caching", "agas_caching": 1},
    # Memory Registration
    {**baseline, "name": "lci_worker_cache", "ndevices": 1, "progress_type": "rp", "reg_mem": 1, "mem_reg_cache": 1},
    {**baseline, "name": "lci_prg_cache", "ndevices": 1, "progress_type": "rp", "reg_mem": 0, "mem_reg_cache": 1},
    {**baseline, "name": "lci_worker_nocache", "ndevices": 1, "progress_type": "rp", "reg_mem": 1, "mem_reg_cache": 0},
    {**baseline, "name": "lci_prg_nocache", "ndevices": 1, "progress_type": "rp", "reg_mem": 0, "mem_reg_cache": 0},
    # old
    # baseline,
    # {**baseline, "name": "lci", "nnodes_list": [2]},
    # {**baseline, "name": "lci", "nnodes_list": [2, 4, 8, 16, 32]},
    # {**baseline, "name": "mpi", "nnodes_list": [2, 4, 8, 16, 32], "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi_sendimm", "nnodes_list": [2, 4, 8, 16, 32], "parcelport": "mpi", "sendimm": 1},
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
    # {**baseline, "name": "mpi", "parcelport": "mpi", "sendimm": 0},
    # {**baseline, "name": "mpi_sendimm", "parcelport": "mpi", "sendimm": 1},
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
                    run_slurm(tag, nnodes, config, time = "3:00")