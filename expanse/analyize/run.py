#!/usr/bin/env python
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
           --account=uic193 \
           --partition=compute \
           --time=00:05:00 \
           --ntasks-per-node=1 \
           slurm.py '{}'
    '''.format(nnodes, job_name, output_filename, output_filename, json.dumps(config))
    os.system(command)

baseline = {
    "name": "lci_putsendrecv_queue_worker_sendimm_l7_async",
    "nnodes_list": [32],
    "task": "rs",
    "parcelport": "lci",
    "max_level": 7,
    "protocol": "putsendrecv",
    "comp_type": "queue",
    "progress_type": "worker",
    "sendimm": 1,
    "backlog_queue": 0,
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
            run(tag, nnodes, config)