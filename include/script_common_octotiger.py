from script_common import *
from platform_config_common import *


def get_default_config():
    default_config = {
        "griddim": 8,
        "zc_threshold": 8192,
        "name": "lci",
        "task": "rs",
        "parcelport": "lci",
        "max_level": 6,
        "protocol": "putva",
        "comp_type": "queue",
        "progress_type": "rp",
        "sendimm": 1,
        "backlog_queue": 0,
        "use_two_device": 0,
        "prg_thread_core": -1,
        "prepost_recv_num": 1,
        "zero_copy_recv": 1,
    }
    return default_config


def get_theta(config):
    griddim = config["griddim"]
    if griddim >= 5:
        theta = 0.34
    elif 3 <= griddim <= 4:
        theta = 0.51
    elif griddim == 2:
        theta = 1.01
    else:
        print("invalid griddim {}!".format(griddim))
        exit(1)
    return theta


def get_nthreads(config):
    platform_config = get_platform_config()
    if config["parcelport"] == "lci" and config["progress_type"] == "pthread":
        nthreads = platform_config["core_num"] - 1
    else:
        nthreads = platform_config["core_num"]
    return nthreads


def get_environ_setting():
    return {
        "LCI_SERVER_MAX_SENDS": "1024",
        "LCI_SERVER_MAX_RECVS": "4096",
        "LCI_SERVER_NUM_PKTS": "65536",
        "LCI_SERVER_MAX_CQES": "65536",
        "LCI_PACKET_SIZE": "12288",
    }


def load_module(config, build_type = "release", enable_pcounter = False):
    module = get_module()
    module("purge")
    if config["griddim"] == 8:
        if build_type == "release":
            octotiger_to_load = "octotiger/master"
        else:
            octotiger_to_load = "octotiger/master-" + build_type
    else:
        octotiger_to_load = "octotiger/local-{}-griddim{}".format(build_type, config["griddim"])
    # Build type
    hpx_to_load = "hpx/local" + "-" + build_type
    lci_to_load = "lci/local" + "-" + build_type
    # Performance counter
    if enable_pcounter:
        lci_to_load += "-pcounter"
    # Thread-safe progress function
    if config["parcelport"] == "lci" and config["progress_type"] == "worker":
        lci_to_load += "-safeprog"

    if hpx_to_load == "hpx/local-release":
        hpx_to_load = "hpx/local"
    if lci_to_load == "lci/local-release":
        lci_to_load = "lci/local"
    module("load", octotiger_to_load)
    module("load", hpx_to_load)
    module("load", lci_to_load)


def get_octotiger_cmd(root_path, config):
    cmd = f'''octotiger \
--hpx:ini=hpx.stacks.use_guard_pages=0 \
--hpx:ini=hpx.parcel.{config["parcelport"]}.priority=1000 \
--hpx:ini=hpx.parcel.{config["parcelport"]}.zero_copy_serialization_threshold={config["zc_threshold"]} \
--config_file={root_path}/data/rotating_star.ini \
--max_level={config["max_level"]} \
--stop_step=5 \
--theta={get_theta(config)} \
--correct_am_hydro=0 \
--disable_output=on \
--monopole_host_kernel_type=LEGACY \
--multipole_host_kernel_type=LEGACY \
--monopole_device_kernel_type=OFF \
--multipole_device_kernel_type=OFF \
--hydro_device_kernel_type=OFF \
--hydro_host_kernel_type=LEGACY \
--amr_boundary_kernel_type=AMR_OPTIMIZED \
--hpx:threads={get_nthreads(config)} \
--hpx:ini=hpx.parcel.lci.protocol={config["protocol"]} \
--hpx:ini=hpx.parcel.lci.comp_type={config["comp_type"]} \
--hpx:ini=hpx.parcel.lci.progress_type={config["progress_type"]} \
--hpx:ini=hpx.parcel.{config["parcelport"]}.sendimm={config["sendimm"]} \
--hpx:ini=hpx.parcel.lci.backlog_queue={config["backlog_queue"]} \
--hpx:ini=hpx.parcel.lci.use_two_device={config["use_two_device"]} \
--hpx:ini=hpx.parcel.lci.prg_thread_core={config["prg_thread_core"]} \
--hpx:ini=hpx.parcel.lci.prepost_recv_num={config["prepost_recv_num"]} \
--hpx:ini=hpx.parcel.zero_copy_receive_optimization={config["zero_copy_recv"]}'''
    return cmd


def run_octotiger(root_path, config, extra_arguments=""):
    os.environ.update(get_environ_setting())

    if config["task"] == "rs":
        cmd = f'''
cd {root_path}/data || exit 1
srun {get_srun_pmi_option(config)} numactl --interleave=all {get_octotiger_cmd(root_path, config)} {extra_arguments}
'''
        print(cmd)
        sys.stdout.flush()
        sys.stderr.flush()
        os.system(cmd)
    else:
        print("Unknown task: " + config["task"])
        exit(1)
