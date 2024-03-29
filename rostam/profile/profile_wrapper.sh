#!/bin/bash

module purge
module load octotiger/master-relWithDebInfo
module load hpx/local-relWithDebInfo
module load lci/local-relWithDebInfo


OCTO_SCRIPT_PATH=${OCTO_SCRIPT_PATH:-/home/jiakun/workspace/octotiger-scripts}
CURRENT_FILE_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${OCTO_SCRIPT_PATH}/data || exit 1
task=${1:-"rs"}
pp=${2:-"lci"}
max_level=${3:-"6"}
mode=${4:-"stat"}

nthreads=40
if [ "$pp" == "lci" ] ; then
#  export LCI_PACKET_RETURN_THRESHOLD=0
#  export LCM_LOG_LEVEL=info
  export LCI_SERVER_MAX_SENDS=1024
  export LCI_SERVER_MAX_RECVS=4096
  export LCI_SERVER_NUM_PKTS=65536
  export LCI_SERVER_MAX_CQES=65536
  export LCI_USE_DREG=1
#  nthreads=127
fi

set -x

if [ "$mode" == "record" ] ; then
  perf record --freq=10 --call-graph dwarf -q -o perf.data.$SLURM_JOB_ID.$SLURM_PROCID \
      numactl --interleave=all octotiger \
              --hpx:ini=hpx.stacks.use_guard_pages=0 \
              --hpx:ini=hpx.parcel.${pp}.priority=1000 \
              --hpx:ini=hpx.parcel.${pp}.zero_copy_serialization_threshold=8192 \
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
              --hpx:threads=${nthreads} \
              --hpx:ini=hpx.parcel.lci.sendimm=1 \
              --hpx:ini=hpx.parcel.lci.rp_prg_pool=1 \
              --hpx:ini=hpx.parcel.lci.backlog_queue=0 \
              --hpx:ini=hpx.parcel.lci.use_two_device=1 \
              --hpx:ini=hpx.parcel.lci.prg_thread_core=-1

  mv ${OCTO_SCRIPT_PATH}/data/perf.data.$SLURM_JOB_ID.$SLURM_PROCID ${CURRENT_FILE_PATH}/data
elif [ "$mode" = "stat" ] ; then
  grep "" /sys/class/infiniband/mlx5_2/ports/1/hw_counters/* > stat.$SLURM_JOB_ID.$SLURM_PROCID.before.log
  perf stat -o stat.$SLURM_JOB_ID.$SLURM_PROCID.stat.log \
       -B -e cache-references,cache-misses,cycles,instructions,branches,branch-misses,faults,migrations \
      octotiger \
              --hpx:ini=hpx.stacks.use_guard_pages=0 \
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
              --hpx:threads=${nthreads} \
              --hpx:ini=hpx.parcel.lci.sendimm=1 \
              --hpx:ini=hpx.parcel.lci.rp_prg_pool=1 \
              --hpx:ini=hpx.parcel.lci.backlog_queue=1 \
              --hpx:ini=hpx.parcel.lci.use_two_device=1 \
              --hpx:ini=hpx.parcel.lci.prg_thread_core=-1
  grep "" /sys/class/infiniband/mlx5_2/ports/1/hw_counters/* > stat.$SLURM_JOB_ID.$SLURM_PROCID.after.log
  mv ${OCTO_SCRIPT_PATH}/data/stat.$SLURM_JOB_ID.$SLURM_PROCID.*.log ${CURRENT_FILE_PATH}/data
  cat ${CURRENT_FILE_PATH}/data/stat.$SLURM_JOB_ID.$SLURM_PROCID.*.log > ${CURRENT_FILE_PATH}/data/stat.$SLURM_JOB_ID.$SLURM_PROCID.log
fi