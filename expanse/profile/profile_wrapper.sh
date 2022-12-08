#!/bin/bash

set -x

module purge
module load DefaultModules
module load octotiger
module load lci-debug

OCTO_SCRIPT_PATH=${OCTO_SCRIPT_PATH:-/home/jackyan1/workspace/octotiger-scripts}
cd ${OCTO_SCRIPT_PATH}/data || exit 1
task=${1:-"rs"}
pp=${2:-"lci"}
max_level=${3:-"6"}

nthreads=128
if [ "$pp" == "lci" ] ; then
#  export LCI_PACKET_RETURN_THRESHOLD=0
  export LCI_USE_DREG=1
  export LCM_LOG_LEVEL=info
  nthreads=127
  SRUN_EXTRA_OPTION="--mpi=pmi2"
elif [ "$pp" == "mpi" ]; then
  SRUN_EXTRA_OPTION="--mpi=pmix"
fi

perf record --freq=10 --call-graph dwarf -q -o perf.data.$SLURM_JOB_ID.$SLURM_PROCID \
    octotiger \
            -Ihpx.stacks.use_guard_pages=0 \
            --hpx:ini=hpx.parcel.${pp}.priority=1000 \
            --hpx:ini=hpx.parcel.${pp}.zero_copy_serialization_threshold=65536 \
            --config_file=${OCTO_SCRIPT_PATH}/data/rotating_star.ini \
            --max_level=${max_level} \
            --stop_step=5 \
            --theta=0.34 \
            --correct_am_hydro=0 \
            --disable_output=on \
            --monopole_host_kernel_type=LEGACY \
            --multipole_host_kernel_type=LEGACY \
            --monopole_device_kernel_type=OFF \
            --multipole_device_kernel_type=OFF \
            --hydro_device_kernel_type=OFF \
            --hydro_host_kernel_type=LEGACY \
            --amr_boundary_kernel_type=AMR_OPTIMIZED \
            --hpx:threads=${nthreads}