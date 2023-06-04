#!/usr/bin/env python
import os
import sys
sys.path.append("../../include")
from script_common import *

import json
import time

# load configuration
default_config = {
    "name": "lci",
    "task": "rs",
    "parcelport": "lci",
    "max_level": 6,
    "protocol": "putva",
    "comp_type": "queue",
    "progress_type": "rp",
    "sendimm": 1,
    "backlog_queue": 0,
}
if len(sys.argv) > 1:
    config=json.loads(sys.argv[1])
else:
    config = default_config
print(config)

# set path
current_path = get_current_script_path()
root_path = os.path.realpath(os.path.join(current_path, "../.."))

# load modules
module = get_module()
module("purge")
module("load", "octotiger/master-release-apex")
if config["parcelport"] == "lci" and config["progress_type"] == "worker":
    module("switch", "--force", "lci", "lci/local-release-safeprog")
module_list()

srun_extra_option = ""
theta = 0.34
zc_threshold = 8192
nthreads = 128
if config["parcelport"] == "lci":
    os.environ["LCI_SERVER_MAX_SENDS"] = "1024"
    os.environ["LCI_SERVER_MAX_RECVS"] = "4096"
    os.environ["LCI_SERVER_NUM_PKTS"] = "65536"
    os.environ["LCI_SERVER_MAX_CQES"] = "65536"
    os.environ["LCI_PACKET_SIZE"] = "12288"
    srun_extra_option = "--mpi=pmi2"
    if config["progress_type"] == "pthread":
        nthreads = 127
elif config["parcelport"] == "mpi":
    srun_extra_option = "--mpi=pmix"
else:
    print("Unknown parcelport type: " + config["parcelport"])
    exit(1)

# Enable APEX
os.environ["APEX_SCREEN_OUTPUT"] = "1"
os.environ["APEX_SCREEN_OUTPUT_DETAIL"] = "1"

if config["task"] == "rs":
    cmd = f'''
cd {root_path}/data || exit 1
srun {srun_extra_option} numactl --interleave=all octotiger \
--hpx:ini=hpx.stacks.use_guard_pages=0 \
--hpx:ini=hpx.parcel.{config["parcelport"]}.priority=1000 \
--hpx:ini=hpx.parcel.{config["parcelport"]}.zero_copy_serialization_threshold={zc_threshold} \
--config_file={root_path}/data/rotating_star.ini \
--max_level={config["max_level"]} \
--stop_step=50 \
--theta={theta} \
--correct_am_hydro=0 \
--disable_output=on \
--monopole_host_kernel_type=LEGACY \
--multipole_host_kernel_type=LEGACY \
--monopole_device_kernel_type=OFF \
--multipole_device_kernel_type=OFF \
--hydro_device_kernel_type=OFF \
--hydro_host_kernel_type=LEGACY \
--amr_boundary_kernel_type=AMR_OPTIMIZED \
--hpx:threads={nthreads} \
--hpx:ini=hpx.parcel.lci.protocol={config["protocol"]} \
--hpx:ini=hpx.parcel.lci.comp_type={config["comp_type"]} \
--hpx:ini=hpx.parcel.lci.progress_type={config["progress_type"]} \
--hpx:ini=hpx.parcel.lci.sendimm={config["sendimm"]} \
--hpx:ini=hpx.parcel.lci.backlog_queue={config["backlog_queue"]} \
--hpx:ini=hpx.parcel.lci.use_two_device={config["use_two_device"]} \
--hpx:ini=hpx.parcel.lci.prg_thread_core={config["prg_thread_core"]}
'''
    print(cmd)
    sys.stdout.flush()
    os.system(cmd)
else:
    print("Unknown task: " + config["task"])
    exit(1)