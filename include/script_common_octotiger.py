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
        "prg_thread_core": -1,
        "prepost_recv_num": 1,
        "zero_copy_recv": 1,
        "match_table_type": "hashqueue",
        "cq_type": "array_atomic_faa",
        "reg_mem": 0,
        "ndevices": 1,
        "ncomps": 1
    }
    return default_config


def get_theta(config):
    griddim = config["griddim"]
    if griddim >= 5:
        theta = 0.34
    elif 3 <= griddim <= 4:
        theta = 0.51
    elif 1 <= griddim <= 2:
        theta = 1.01
    else:
        print("invalid griddim {}!".format(griddim))
        exit(1)
    return theta


def get_nthreads(config):
    core_num = get_platform_config("core_num", required=True)
    if config["parcelport"] == "lci" and "pthread" in config["progress_type"]:
        nthreads = core_num - 1
    else:
        nthreads = core_num
    return nthreads


def get_environ_setting(config):
    ret = {
        "LCI_SERVER_MAX_SENDS": "1024",
        "LCI_SERVER_MAX_RECVS": "4096",
        "LCI_SERVER_NUM_PKTS": "65536",
        "LCI_SERVER_MAX_CQES": "65536",
        "LCI_PACKET_SIZE": "12288",
    }
    if "match_table_type" in config:
        ret["LCI_MT_BACKEND"] = config["match_table_type"]
    if "cq_type" in config:
        ret["LCI_CQ_TYPE"] = config["cq_type"]
    if "reg_mem" in config and config["reg_mem"] or config["progress_type"] == "worker":
        # We only use the registration cache when only one progress thread is doing the registration.
        ret["LCI_USE_DREG"] = "0"
    if "mem_reg_cache" in config:
        ret["LCI_USE_DREG"] = str(config["mem_reg_cache"])
    return ret


def load_module(config, build_type = "release", enable_pcounter = False, extra=None):
    module = get_module()
    module("purge")
    octotiger_major = get_platform_config("octotiger_major")
    if octotiger_major is None:
        octotiger_major = "local"
    octotiger_base = "octotiger/{}".format(octotiger_major)
    if config["griddim"] == 8:
        if build_type == "release":
            octotiger_to_load = octotiger_base
        else:
            octotiger_to_load = octotiger_base + "-" + build_type
    else:
        octotiger_to_load = octotiger_base + "-{}-griddim{}".format(build_type, config["griddim"])
    # Build type
    hpx_to_load = "hpx/local" + "-" + build_type
    lci_to_load = "lci/local" + "-" + build_type
    # Performance counter
    if enable_pcounter:
        hpx_to_load += "-pcounter"
        lci_to_load += "-pcounter"
    # Thread-safe progress function
    if config["parcelport"] == "lci" and "worker" in config["progress_type"]:
        lci_to_load += "-safeprog"

    if hpx_to_load == "hpx/local-release":
        hpx_to_load = "hpx/local"
    if lci_to_load == "lci/local-release":
        lci_to_load = "lci/local"
    module("load", octotiger_to_load)
    module("load", hpx_to_load)
    module("load", lci_to_load)
    if extra:
        if type(extra) is not list:
            extra = [extra]
        for t in extra:
            module("load", t)


def get_octotiger_cmd(root_path, config):
    prg_thread_num = 1
    if "prg_thread_num" in config:
        if config["prg_thread_num"] == "auto":
            prg_thread_num = config["ndevices"]
        else:
            prg_thread_num = config["prg_thread_num"]

    agas_use_caching = 0
    if "agas_caching" in config:
        agas_use_caching = config["agas_caching"]

    if config["task"] == "rs":
        config_filename = "rotating_star.ini"
    elif config["task"] == "gr":
        config_filename = "sphere.ini"
    else:
        print("Unknown task!")
        exit(1)

    stop_step = 5
    if "stop_step" in config:
        stop_step = config["stop_step"]

    cmd = f'''octotiger \
--hpx:ini=hpx.stacks.use_guard_pages=0 \
--hpx:ini=hpx.parcel.{config["parcelport"]}.priority=1000 \
--hpx:ini=hpx.parcel.{config["parcelport"]}.zero_copy_serialization_threshold={config["zc_threshold"]} \
--config_file={root_path}/data/{config_filename} \
--max_level={config["max_level"]} \
--stop_step={stop_step} \
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
--hpx:ini=hpx.agas.use_caching={agas_use_caching} \
--hpx:ini=hpx.parcel.lci.protocol={config["protocol"]} \
--hpx:ini=hpx.parcel.lci.comp_type={config["comp_type"]} \
--hpx:ini=hpx.parcel.lci.progress_type={config["progress_type"]} \
--hpx:ini=hpx.parcel.{config["parcelport"]}.sendimm={config["sendimm"]} \
--hpx:ini=hpx.parcel.lci.backlog_queue={config["backlog_queue"]} \
--hpx:ini=hpx.parcel.lci.prepost_recv_num={config["prepost_recv_num"]} \
--hpx:ini=hpx.parcel.zero_copy_receive_optimization={config["zero_copy_recv"]} \
--hpx:ini=hpx.parcel.lci.reg_mem={config["reg_mem"]} \
--hpx:ini=hpx.parcel.lci.ndevices={config["ndevices"]} \
--hpx:ini=hpx.parcel.lci.prg_thread_num={prg_thread_num} \
--hpx:ini=hpx.parcel.lci.ncomps={config["ncomps"]}'''
    return cmd


def run_octotiger(root_path, config, extra_arguments=""):
    os.environ.update(get_environ_setting(config))
    platform_config = get_platform_config_all()
    numactl_cmd = ""
    if platform_config["numa_policy"] == "interleave":
        numactl_cmd = "numactl --interleave=all"

    cmd = f'''
cd {root_path}/data || exit 1
srun {get_srun_pmi_option(config)} {numactl_cmd} {get_octotiger_cmd(root_path, config)} {extra_arguments}
'''
    print(cmd)
    sys.stdout.flush()
    sys.stderr.flush()
    os.system(cmd)
