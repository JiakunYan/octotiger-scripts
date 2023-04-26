#!/bin/bash
#SBATCH --partition=medusa
#SBATCH --time=00:05:00
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=debug

module purge
module load octotiger
#module load hpx/local-relWithDebInfo
#module load lci/local-release-pcounter
module load lci/local-release-safeprog
#module load lci/local-relWithDebInfo-safeprog
#module load lci/local-debug-safeprog
#module load libibverbs/local-debug
module list

OCTO_SCRIPT_PATH=${OCTO_SCRIPT_PATH:-/home/jiakun/workspace/octotiger-scripts}

cd ${OCTO_SCRIPT_PATH}/data || exit 1
task=${1:-"rs"}
pp=${2:-"lci"}
max_level=${3:-"3"}

set -x

nthreads=40
if [ "$pp" == "lci" ] ; then
#  export LCI_PACKET_RETURN_THRESHOLD=0
#  export LCI_IBV_USE_ODP=1
#  export LCI_TOUCH_LBUFFER=0
#  export LCI_IBV_USE_PREFETCH=0
#  export LCM_LOG_LEVEL=trace
#  export LCM_LOG_WHITELIST="monitor"
#  export LCM_LOG_WHITELIST="server;device;bq;monitor;env"
#  export LCM_LOG_OUTFILE=$LOG_OUTPUT_PATH/debug.$SLURM_JOB_ID.%.log
#  export LCM_LOG_OUTFILE=stdout
#  export LCM_LOG_LEVEL=info
#  export LCI_ENABLE_MONITOR_THREAD=1
#  export LCI_MONITOR_THREAD_INTERVAL=10
  export LCI_SERVER_MAX_SENDS=1024
  export LCI_SERVER_MAX_RECVS=4096
  export LCI_SERVER_NUM_PKTS=65536
  export LCI_SERVER_MAX_CQES=65536
#  export LCI_USE_DREG=0
#  export LCI_IBV_ENABLE_EVENT_POLLING_THREAD=0
fi

# Run the job
date
echo "run $task with parcelport $pp nthreads ${nthreads}; max_level=${max_level} tag=${RUN_TAG}"

ulimit -c unlimited
if [ "$task" = "rs" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
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
        --hpx:ini=hpx.parcel.lci.protocol=putva \
        --hpx:ini=hpx.parcel.lci.comp_type=queue \
        --hpx:ini=hpx.parcel.lci.progress_type=worker \
        --hpx:ini=hpx.parcel.lci.sendimm=1 \
        --hpx:ini=hpx.parcel.lci.backlog_queue=0 \
        --hpx:ini=hpx.parcel.lci.use_two_device=0 \
        --hpx:ini=hpx.parcel.lci.prg_thread_core=-1
elif [ "$task" = "dwd" ] ; then
  srun ${SRUN_EXTRA_OPTION} octotiger \
        --hpx:ini=hpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --config_file=${OCTO_SCRIPT_PATH}/data/dwd.ini \
        --monopole_host_kernel_type=LEGACY \
        --multipole_host_kernel_type=LEGACY \
        --monopole_device_kernel_type=CUDA \
        --multipole_device_kernel_type=CUDA \
        --hydro_device_kernel_type=CUDA \
        --hydro_host_kernel_type=LEGACY \
        --cuda_streams_per_gpu=128 \
        --cuda_buffer_capacity=2 \
        --hpx:threads=${nthreads}
elif [ "$task" = "gr" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
        --hpx:ini=hpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --config_file=${OCTO_SCRIPT_PATH}/data/sphere.ini \
        --max_level=${max_level} \
        --stop_step=10 \
        --theta=0.34 \
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
elif [ "$task" = "hy" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
        --hpx:ini=hpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --config_file=${OCTO_SCRIPT_PATH}/data/blast.ini \
        --max_level=${max_level} \
        --stop_step=10 \
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
fi