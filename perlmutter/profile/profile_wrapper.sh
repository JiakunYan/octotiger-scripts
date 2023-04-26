#!/bin/bash

set -x

module purge
module load octotiger

OCTO_SCRIPT_PATH=${OCTO_SCRIPT_PATH:-/global/homes/j/jackyan/workspace/octotiger-scripts}
cd ${OCTO_SCRIPT_PATH}/data || exit 1
task=${1:-"rs"}
pp=${2:-"lci"}
max_level=${3:-"3"}

nthreads=64
if [ "$pp" == "lci" ] ; then
#  export LCI_PACKET_RETURN_THRESHOLD=0
  export LCM_LOG_LEVEL=info
  nthreads=63
  SRUN_EXTRA_OPTION="--mpi=pmi2"
elif [ "$pp" == "mpi" ]; then
  SRUN_EXTRA_OPTION="--mpi=pmix"
fi

perf record --freq=10 --call-graph dwarf -q -o perf.data.$SLURM_JOB_ID.$SLURM_PROCID \
    octotiger \
            --hpx:ini=hpx.stacks.use_guard_pages=0 \
            --hpx:ini=hpx.parcel.${pp}.priority=1000 \
            --hpx:ini=hpx.parcel.${pp}.zero_copy_serialization_threshold=8192 \
            --config_file=${OCTO_SCRIPT_PATH}/data/rotating_star.ini \
            --max_level=${max_level} \
            --stop_step=5 \
            --theta=0.34 \
            --correct_am_hydro=0 \
            --cuda_number_gpus=1 \
            --disable_output=on \
            --cuda_streams_per_gpu=128 \
            --cuda_buffer_capacity=1 \
            --monopole_host_kernel_type=DEVICE_ONLY \
            --multipole_host_kernel_type=DEVICE_ONLY \
            --monopole_device_kernel_type=CUDA \
            --multipole_device_kernel_type=CUDA \
            --hydro_device_kernel_type=CUDA \
            --hydro_host_kernel_type=DEVICE_ONLY \
            --amr_boundary_kernel_type=AMR_OPTIMIZED \
            --hpx:threads=${nthreads}