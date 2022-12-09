#!/usr/bin/env bash

# exit when any command fails
set -e
# import the the script containing common functions
source ../../include/scripts.sh

# get the root path via environment variable or default value
OCTO_SCRIPT_PATH=$(realpath "${OCTO_SCRIPT_PATH:-../../}")
export OCTO_SCRIPT_PATH

tasks=("rs")
max_levels=("6")
#nnodes=(2 4 8 16 32)
#pps=("lci" "mpi")
nnodes=(2)
pps=("lci")

# create the ./log directory
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
               --output=./run/slurm_output.%x.j%j.out \
               --error=./run/slurm_output.%x.j%j.out \
               run.slurm $t $p $max_level || { echo "sbatch error!"; exit 1; }
      done
    done
  done
done
cd ..