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
    "name": "lci",
    "nnodes_list": [32],
    "task": "rs",
    "parcelport": "lci",
    "max_level": 6,
    "protocol": "putva",
    "comp_type": "queue",
    "progress_type": "rp",
    "sendimm": 1,
    "backlog_queue": 0,
    "use_two_device": 0,
    "prg_thread_core": -1
}

configs = [
    # baseline,
    # {**baseline, "name": "mpi", "parcelport": "mpi"},
    # {**baseline, "name": "sendrecv", "protocol": "sendrecv"},
    # {**baseline, "name": "sync", "comp_type": "sync"},
    # {**baseline, "name": "progress_pthread", "progress_type": "pthread"},
    # {**baseline, "name": "progress_worker", "progress_type": "worker"},
    # {**baseline, "name": "no_sendimm", "sendimm": 0},
    # {**baseline, "name": "backlog_queue", "backlog_queue": 1},
    # {**baseline, "name": "use_two_device", "use_two_device": 1},
    {**baseline, "name": "test", "nnodes_list": [1], "max_level": 5},
]

if __name__ == "__main__":
    mkdir_s("./run")

    tag = getenv_or("RUN_TAG", "default")
    os.environ["CURRENT_SCRIPT_PATH"] = os.path.dirname(os.path.realpath(__file__))
    for config in configs:
        # print(config)
        for nnodes in config["nnodes_list"]:
            run(tag, nnodes, config)