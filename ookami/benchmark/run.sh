#!/usr/bin/env bash

# exit when any command fails
set -e
# import the the script containing common functions
source ../../include/scripts.sh

CURRENT_SCRIPT_PATH=$(realpath "$(dirname "$0")")
OCTO_SCRIPT_PATH=$(realpath "${CURRENT_SCRIPT_PATH}/../..")
export OCTO_SCRIPT_PATH

# get the root path via environment variable or default value
tasks=("rs")
max_levels=("5")
nnodes=(64 128)
pps=("lci" "mpi")

# create the ./run directory
mkdir_s ./run

for j in $(eval echo {1..${1:-1}}); do
  for i in "${!tasks[@]}"; do
    t=${tasks[i]}
    max_level=${max_levels[i]}
    for n in "${nnodes[@]}"; do
      if [ $n -gt 80 ]
      then
        queue="all-nodes"
      elif [ $n -gt 40 ]
      then
        queue="large"
      elif [ $n -gt 32 ]
      then
        queue="medium"
      else
        queue="short"
      fi

      for p in "${pps[@]}"; do
        name=debug-$t-$p-n$n-l$max_level
        sbatch --nodes=$n \
               --job-name=$name \
               --partition=$queue \
               --output=./run/slurm_output.%x.j%j.out \
               --error=./run/slurm_output.%x.j%j.out \
               run.slurm $t $p $max_level || { echo "sbatch error!"; exit 1; }
      done
    done
  done
done
cd ..