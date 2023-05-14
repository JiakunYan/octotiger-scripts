#!/usr/bin/env python
import os
import sys
sys.path.append(f'{os.environ["HOME"]}/workspace/octotiger-scripts/include')
from script_common_octotiger import *
import json

# load configuration
config = get_default_config()
if len(sys.argv) > 1:
    config.update(json.loads(sys.argv[1]))
print("Config: " + json.dumps(config))

# set path
current_path = get_current_script_path()
root_path = os.path.realpath(os.path.join(current_path, "../.."))

# load modules
load_module(config, "relWithDebInfo")
module_list()

perf_output = f'perf.data.{os.environ["SLURM_JOB_ID"]}.{os.environ["SLURM_PROCID"]}'
cmd = f'''
cd {root_path}/data || exit 1
perf record --freq=10 --call-graph dwarf -q -o {perf_output} \
      numactl --interleave=all {get_octotiger_cmd(root_path, config)} \
'''
print(cmd)
sys.stdout.flush()
sys.stderr.flush()
os.system(cmd)
os.rename(f"{root_path}/data/{perf_output}", f"{current_path}/run/{perf_output}")