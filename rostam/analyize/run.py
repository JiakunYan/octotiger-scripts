#!/usr/bin/env python3
import sys
sys.path.append("../../include")
from script_common import *
import json

def run(tag, nnodes, config):
    job_name="n{}-{}".format(nnodes, config["name"])
    output_filename = "./run/slurm_output.{}.%x.j%j.out".format(tag)
    command = '''
    sbatch --export=ALL \
           --nodes={} \
           --job-name={} \
           --output={} \
           --error={} \
           --partition=medusa \
           --time=00:05:00 \
           --ntasks-per-node=1 \
           slurm.py '{}'
    '''.format(nnodes, job_name, output_filename, output_filename, json.dumps(config))
    os.system(command)

baseline = {
    "name": "lci-dim8",
    "nnodes_list": [8],
    "max_level": 5,
    "griddim": 8,
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
    baseline,
]

if __name__ == "__main__":
    mkdir_s("run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    for config in configs:
        # print(config)
        for nnodes in config["nnodes_list"]:
            run(tag, nnodes, config)