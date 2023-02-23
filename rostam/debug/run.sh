#!/usr/bin/env bash

# exit when any command fails
set -e
# import the the script containing common functions
source ../../include/scripts.sh

CURRENT_SCRIPT_PATH=$(realpath "$(dirname "$0")")
OCTO_SCRIPT_PATH=$(realpath "${CURRENT_SCRIPT_PATH}/../..")
export OCTO_SCRIPT_PATH
export RUN_TAG=${RUN_TAG:-default}

# get the root path via environment variable or default value
tasks=("rs")
max_levels=("5")
nnodes=(8)
pps=("lci")

# create the ./run directory
mkdir_s ./run

for i in $(eval echo {1..${1:-1}}); do
  for i in "${!tasks[@]}"; do
    t=${tasks[i]}
    max_level=${max_levels[i]}
    for n in "${nnodes[@]}"; do
      for p in "${pps[@]}"; do
        name=$t-$p-n$n-l$max_level
        sbatch --nodes=$n \
               --job-name=$name \
               --output=./run/slurm_output.%x.${RUN_TAG}.j%j.out \
               --error=./run/slurm_output.%x.${RUN_TAG}.j%j.out \
               run.slurm $t $p $max_level || { echo "sbatch error!"; exit 1; }
      done
    done
  done
done
cd ..