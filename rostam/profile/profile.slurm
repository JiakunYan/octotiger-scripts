#!/bin/bash
#SBATCH --partition=medusa
#SBATCH --time=00:15:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=profile
#SBATCH --output=slurm_output.%x-o%j
#SBATCH --error=slurm_error.%x-o%j

task="rs"
pp="lci"
max_level="5"
mode=${1:-"stat"}
if [ "$pp" == "lci" ] ; then
  SRUN_EXTRA_OPTION="--mpi=pmi2"
elif [ "$pp" == "mpi" ]; then
  SRUN_EXTRA_OPTION="--mpi=pmix"
fi

srun ${SRUN_EXTRA_OPTION} bash ${ROOT_PATH}/profile_wrapper.sh $task $pp $max_level $mode