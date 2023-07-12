def get_platform_config():
    return {
        "name": "perlmutter",
        "core_num": 64,
        "best numa policy": "default",
    }

def get_srun_pmi_option(config):
    srun_pmi_option = "--mpi=pmix"
    return srun_pmi_option