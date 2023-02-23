#!/bin/bash

# exit when any command fails
set -e
# import the the script containing common functions
source ../../include/scripts.sh

ROOT_PATH=$(realpath "${ROOT_PATH:-.}")
export ROOT_PATH=$ROOT_PATH

if [[ -d "${ROOT_PATH}" ]]; then
  echo "Run LCI profile at ${ROOT_PATH}"
else
  echo "Did not find profile at ${ROOT_PATH}!"
  exit 1
fi

# create the ./run directory
mkdir_s ./data
cd data

#mode=${1:-"stat"}
mode=${1:-"record"}

sbatch ${ROOT_PATH}/profile.slurm $mode || { echo "sbatch error!"; exit 1; }
cd ..