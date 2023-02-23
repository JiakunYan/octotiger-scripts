#!/bin/bash
#SBATCH --account=uic193
#SBATCH --partition=compute
#SBATCH --time=00:05:00
#SBATCH --ntasks-per-node=1

module purge
module load octotiger
module load lci/local

OCTO_SCRIPT_PATH=${OCTO_SCRIPT_PATH:-/home/jackyan1/workspace/octotiger-scripts}
cd ${OCTO_SCRIPT_PATH}/data || exit 1
task=${1:-"rs"}
pp=${2:-"lci"}
max_level=${3:-"3"}

nthreads=128
if [ "$pp" == "lci" ] ; then
  export LCI_SERVER_MAX_SENDS=1024
  export LCI_SERVER_MAX_RECVS=4096
  export LCI_SERVER_NUM_PKTS=65536
  export LCI_SERVER_MAX_CQES=65536
  export LCI_USE_DREG=1
#  nthreads=127
  SRUN_EXTRA_OPTION="${SRUN_EXTRA_OPTION} --mpi=pmi2"
elif [ "$pp" == "mpi" ]; then
  SRUN_EXTRA_OPTION="${SRUN_EXTRA_OPTION} --mpi=pmix"
fi

# Run the job
date
echo "run $task with parcelport $pp nthreads ${nthreads}; max_level=${max_level} tag=${RUN_TAG}"

if [ "$task" = "rs" ] ; then
	srun ${SRUN_EXTRA_OPTION} numactl --interleave=all octotiger \
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
        --hpx:ini=hpx.parcel.lci.backlog_queue=1 \
        --hpx:ini=hpx.parcel.lci.use_two_device=1 \
        --hpx:ini=hpx.parcel.lci.prg_thread_core=-1
#        --hpx:ini=hpx.parcel.lci.numa_interleave=0
elif [ "$task" = "dwd" ] ; then
  srun ${SRUN_EXTRA_OPTION} octotiger \
        --hpx:ini=hpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --hpx:ini=hpx.parcel.${pp}.zero_copy_serialization_threshold=65536 \
        --config_file=${OCTO_SCRIPT_PATH}/data/dwd.ini \
        --monopole_host_kernel_type=LEGACY \
        --multipole_host_kernel_type=LEGACY \
        --monopole_device_kernel_type=OFF \
        --multipole_device_kernel_type=OFF \
        --hydro_device_kernel_type=OFF \
        --hydro_host_kernel_type=LEGACY \
        --amr_boundary_kernel_type=AMR_OPTIMIZED \
        --hpx:threads=${nthreads}
elif [ "$task" = "gr" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
        --hpx:ini=hpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --hpx:ini=hpx.parcel.${pp}.zero_copy_serialization_threshold=65536 \
        --config_file=${OCTO_SCRIPT_PATH}/data/sphere.ini \
        --max_level=${max_level} \
        --stop_step=10 \
        --theta=0.34 \
        --disable_output=on \
        --monopole_host_kernel_type=LEGACY \
        --multipole_host_kernel_type=LEGACY \
        --monopole_device_kernel_type=OFF \
        --multipole_device_kernel_type=OFF \
        --hydro_device_kernel_type=OFF \
        --hydro_host_kernel_type=LEGACY \
        --amr_boundary_kernel_type=AMR_OPTIMIZED \
        --hpx:threads=${nthreads}
elif [ "$task" = "hy" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
        --hpx:ini=hpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --hpx:ini=hpx.parcel.${pp}.zero_copy_serialization_threshold=65536 \
        --config_file=${OCTO_SCRIPT_PATH}/data/blast.ini \
        --max_level=${max_level} \
        --stop_step=10 \
        --disable_output=on \
        --monopole_host_kernel_type=LEGACY \
        --multipole_host_kernel_type=LEGACY \
        --monopole_device_kernel_type=OFF \
        --multipole_device_kernel_type=OFF \
        --hydro_device_kernel_type=OFF \
        --hydro_host_kernel_type=LEGACY \
        --amr_boundary_kernel_type=AMR_OPTIMIZED \
        --hpx:threads=${nthreads}
fi