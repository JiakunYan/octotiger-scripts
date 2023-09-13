#!/usr/bin/env python3
import os
import sys
sys.path.append("../../include")
from script_common_octotiger import *

import json
import time

# load configuration
config = get_default_config()
if len(sys.argv) > 1:
    config.update(json.loads(sys.argv[1]))
print("Config: " + json.dumps(config))

# load configuration
config = get_default_config()
if len(sys.argv) > 1:
    config.update(json.loads(sys.argv[1]))
print("Config: " + json.dumps(config))

# set path
current_path = get_current_script_path()
root_path = os.path.realpath(os.path.join(current_path, "../.."))

# load modules
extra_modules = ["hpx/local-release-pcounter"]
if config["progress_type"] == "worker":
    extra_modules.append("lci/local-release-safeprog")
load_module(config, build_type="release", enable_pcounter=0, extra=extra_modules)
module_list()

# os.environ["LCM_LOG_LEVEL"] = "trace"
# extra_arguments = f'''\
# --hpx:ini=hpx.parcel.lci.log_level=profile \
# --hpx:ini=hpx.parcel.lci.log_outfile={current_path}/run/octotiger_trace.{config["name"]}.%.log \
# --enable_trace=1
# '''
# run_octotiger(root_path, config, extra_arguments=extra_arguments)
os.environ["HPX_LCI_LOG_LEVEL"] = "profile"
os.environ["HPX_LCI_LOG_OUTFILE"] = f'{current_path}/run/octotiger_trace.{config["name"]}.%.log'
run_octotiger(root_path, config)
