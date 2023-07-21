#!/usr/bin/env python
import os
import sys
sys.path.append("../../include")
from script_common_octotiger import *
import json

# load configuration
config = get_default_config()
if len(sys.argv) > 1:
    config = json.loads(sys.argv[1])

if type(config) is list:
    configs = config
else:
    configs = [config]

# set path
current_path = get_current_script_path()
root_path = os.path.realpath(os.path.join(current_path, "../.."))

for config in configs:
    print("Config: " + json.dumps(config))
    # load modules
    load_module(config)
    module_list()

    run_octotiger(root_path, config)