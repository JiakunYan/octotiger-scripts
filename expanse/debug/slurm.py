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
    load_module(config, build_type="release", enable_pcounter=False)
    module_list()

    # os.environ["LCT_PCOUNTER_RECORD_INTERVAL"] = "1000" # record every 1 ms
    # os.environ["LCT_PCOUNTER_AUTO_DUMP"] = "pcounter.log.%"
    os.environ["LCI_IBV_ENABLE_TD"] = "0"
    extra_arguments = ""
    # os.environ["LCI_USE_DREG"] = "0"
    # extra_arguments = "--hpx:ini=hpx.parcel.zero_copy_optimization=0"
    run_octotiger(root_path, config, extra_arguments=extra_arguments)
    mv(os.path.join(root_path, "data/pcounter*"), os.path.join(current_path, "run"))