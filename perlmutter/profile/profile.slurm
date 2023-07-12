#!/bin/bash
#SBATCH --account=xpress_g
#SBATCH --constraint=gpu
#SBATCH --qos=regular
#SBATCH --time=00:05:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --gpus-per-task=4
#SBATCH --gpu-bind=map_gpu:0,1,2,3
#SBATCH --threads-per-core=1
#SBATCH --hint=nomultithread
#SBATCH --job-name=profile
#SBATCH --output=slurm_output.%x-o%j
#SBATCH --error=slurm_output.%x-o%j

srun bash ${ROOT_PATH}/profile_wrapper.sh