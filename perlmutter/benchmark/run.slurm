#!/bin/bash
#SBATCH -A xpress_g
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -t 00:05:00
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=16
#SBATCH --gpus-per-task=1
#SBATCH --gpu-bind=map_gpu:0,1

module purge
module load octotiger

OCTO_SCRIPT_PATH=${OCTO_SCRIPT_PATH:-/global/homes/j/jackyan/workspace/octotiger-scripts}

cd ${OCTO_SCRIPT_PATH}/data || exit 1
task=${1:-"rs"}
pp=${2:-"lci"}
max_level=${3:-"3"}

if [ "$pp" == "lci" ] ; then
  export LCI_SERVER_MAX_SENDS=64
  export LCI_SERVER_MAX_RECVS=4096
  export LCI_SERVER_NUM_PKTS=65536
  export LCI_SERVER_MAX_CQES=65536
  SRUN_EXTRA_OPTION="${SRUN_EXTRA_OPTION} --mpi=pmi2"
fi

# Run the job
date
echo "run $task with parcelport $pp; max_level=${max_level}"

if [ "$task" = "rs" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
        -Ihpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --config_file=${OCTO_SCRIPT_PATH}/data/rotating_star.ini \
        --max_level=5 \
        --stop_step=10 \
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
        --amr_boundary_kernel_type=AMR_OPTIMIZED
elif [ "$task" = "dwd" ] ; then
  srun ${SRUN_EXTRA_OPTION} octotiger \
        -Ihpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --config_file=${OCTO_SCRIPT_PATH}/data/dwd.ini \
        --monopole_host_kernel_type=LEGACY \
        --multipole_host_kernel_type=LEGACY \
        --monopole_device_kernel_type=CUDA \
        --multipole_device_kernel_type=CUDA \
        --hydro_device_kernel_type=CUDA \
        --hydro_host_kernel_type=LEGACY \
        --cuda_streams_per_gpu=128 \
        --cuda_buffer_capacity=2
elif [ "$task" = "gr" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
        -Ihpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --config_file=${OCTO_SCRIPT_PATH}/data/sphere.ini \
        --max_level=5 \
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
        --amr_boundary_kernel_type=AMR_OPTIMIZED
elif [ "$task" = "hy" ] ; then
	srun ${SRUN_EXTRA_OPTION} octotiger \
        -Ihpx.stacks.use_guard_pages=0 \
        --hpx:ini=hpx.parcel.${pp}.priority=1000 \
        --config_file=${OCTO_SCRIPT_PATH}/data/blast.ini \
        --max_level=10 \
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
        --amr_boundary_kernel_type=AMR_OPTIMIZED
fi