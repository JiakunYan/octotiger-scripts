#!/usr/bin/env python3
#SBATCH --cpus-per-task=128

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
load_module(config, build_type="release", enable_pcounter=False)
module_list()

os.environ["LCT_PCOUNTER_RECORD_INTERVAL"] = "1000" # record every 1 ms
os.environ["LCT_PCOUNTER_AUTO_DUMP"] = "pcounter.log.%"
extra_arguments = ""
# os.environ["LCI_LOG_LEVEL"] = "debug"
os.environ["LCI_OFI_PROVIDER_HINT"] = "sockets"
run_octotiger(root_path, config, extra_arguments=extra_arguments)
mv(os.path.join(root_path, "data/pcounter*"), os.path.join(current_path, "run"))