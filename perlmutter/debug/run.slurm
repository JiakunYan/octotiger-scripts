#!/bin/bash
#SBATCH --account=xpress_g
#SBATCH --constraint=gpu
#SBATCH --qos=regular
#SBATCH --time=00:01:00
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=16
#SBATCH --gpus-per-task=1
#SBATCH --gpu-bind=map_gpu:0,1,2,3
#SBATCH --threads-per-core=1
#SBATCH --hint=nomultithread

module purge
module load octotiger
#module load hpx/local-release-pcounter
#module load lci/local-release-pcounter
#module load lci/local-debug
module list

OCTO_SCRIPT_PATH=${OCTO_SCRIPT_PATH:-/global/homes/j/jackyan/workspace/octotiger-scripts}

cd ${OCTO_SCRIPT_PATH}/data || exit 1
task=${1:-"rs"}
pp=${2:-"lci"}
max_level=${3:-"3"}

if [ "$pp" == "lci" ] ; then
#  export LCI_LOG_LEVEL=debug
  export LCI_SERVER_MAX_SENDS=256
  export LCI_SERVER_MAX_RECVS=4096
  export LCI_SERVER_NUM_PKTS=65536
  export LCI_SERVER_MAX_CQES=8192
  export LCI_PACKET_SIZE=65536
fi
SRUN_EXTRA_OPTION=""
#export FI_CXI_RX_MATCH_MODE=software
#export FI_CXI_DEFAULT_CQ_SIZE=1310720
#  export FI_MR_CACHE_MONITOR=memhooks
#export APEX_DISABLE=1
#export APEX_SCREEN_OUTPUT=1
#export APEX_ENABLE_CUDA=1
export PMI_MAX_KVS_ENTRIES=128

#export LCT_PCOUNTER_AUTO_DUMP="pcounter.log.%"

#srun octotiger \
#  --hydro_device_kernel_type=CUDA \
#  --hydro_host_kernel_type=DEVICE_ONLY \
#  --amr_boundary_kernel_type=AMR_OPTIMIZED \
#  --max_executor_slices=8 \
#  --cuda_streams_per_gpu=32 \
#  --config_file=${OCTO_SCRIPT_PATH}/data/blast.ini \
#  --unigrid=1 --disable_output=on \
#  --max_level=5 \
#  --stop_step=15 \
#  --stop_time=25 \
#  --optimize_local_communication=1 \
#  --hpx:ini=hpx.stacks.use_guard_pages!=0 \
#  --hpx:ini=hpx.parcel.${pp}.priority=1000 \
#  --hpx:ini=hpx.parcel.${pp}.enable=1 \
#  --hpx:ini=hpx.parcel.bootstrap=${pp} \
#  --hpx:ini=hpx.parcel.lci.protocol=putva
#exit 0

# Run the job
date
echo "run $task with parcelport $pp; max_level=${max_level}"

export LCI_ENABLE_PRG_NET_ENDPOINT=0

if [ "$task" = "rs" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
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
        --hpx:threads=16 \
        --hpx:ini=hpx.parcel.lci.protocol=putva \
        --hpx:ini=hpx.agas.use_caching=0 \
        --hpx:ini=hpx.parcel.lci.progress_type=rp \
        --hpx:ini=hpx.parcel.lci.ndevices=1 \
        --hpx:ini=hpx.parcel.lci.prg_thread_num=1
fi