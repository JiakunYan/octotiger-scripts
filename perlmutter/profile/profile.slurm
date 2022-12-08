#!/bin/bash
#SBATCH --constraint=gpu
#SBATCH --account=xpress_g
#SBATCH --qos=regular
#SBATCH --time=5:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=profile
#SBATCH --output=slurm_output.%x-o%j
#SBATCH --error=slurm_output.%x-o%j

srun --mpi=pmi2 bash ${ROOT_PATH}/profile_wrapper.sh