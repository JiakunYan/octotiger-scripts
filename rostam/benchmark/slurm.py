#!/usr/bin/env python3
import os
import sys
sys.path.append("../../include")
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
load_module(config, build_type="release", enable_pcounter=False, extra=["ucx"])
module_list()

run_octotiger(root_path, config)
