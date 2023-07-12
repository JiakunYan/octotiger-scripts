#!/bin/bash

set -x

module purge
module load octotiger

OCTO_SCRIPT_PATH=${OCTO_SCRIPT_PATH:-/global/homes/j/jackyan/workspace/octotiger-scripts}
cd ${OCTO_SCRIPT_PATH}/data || exit 1
task=${1:-"rs"}
pp=${2:-"lci"}
max_level=${3:-"4"}

if [ "$pp" == "lci" ] ; then
  export LCI_LOG_LEVEL=info
  export LCI_SERVER_MAX_SENDS=256
  export LCI_SERVER_MAX_RECVS=4096
  export LCI_SERVER_NUM_PKTS=65536
  export LCI_SERVER_MAX_CQES=8192
  export LCI_PACKET_SIZE=12288
fi
export FI_CXI_RX_MATCH_MODE=software
export FI_CXI_DEFAULT_CQ_SIZE=1310720
#  export FI_MR_CACHE_MONITOR=memhooks
export APEX_DISABLE=1
export APEX_SCREEN_OUTPUT=1
export APEX_ENABLE_CUDA=1

perf record --freq=10 --call-graph dwarf -q -o perf.data.$SLURM_JOB_ID.$SLURM_PROCID \
	octotiger \
        --hpx:ini=hpx.stacks.use_guard_pages!=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --hpx:ini=hpx.parcel.${pp}.zero_copy_serialization_threshold=8192 \
        --config_file=${OCTO_SCRIPT_PATH}/data/rotating_star.ini \
        --max_level=${max_level} \
        --stop_step=5 \
        --theta=0.34 \
        --correct_am_hydro=0 \
        --disable_output=on \
        --max_executor_slices=8 \
        --cuda_streams_per_gpu=32 \
        --monopole_host_kernel_type=DEVICE_ONLY \
        --multipole_host_kernel_type=DEVICE_ONLY \
        --monopole_device_kernel_type=CUDA \
        --multipole_device_kernel_type=CUDA \
        --hydro_device_kernel_type=CUDA \
        --hydro_host_kernel_type=DEVICE_ONLY \
        --amr_boundary_kernel_type=AMR_OPTIMIZED \
        --hpx:ini=hpx.parcel.lci.protocol=putva

mv ${OCTO_SCRIPT_PATH}/data/perf.data.* ${ROOT_PATH}/data