#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --job-name=test
#SBATCH --ntasks-per-node=1
#SBATCH --partition=short
#SBATCH --output=./run/slurm_output.%x.j%j.out
#SBATCH --error=./run/slurm_output.%x.j%j.out


module purge
module load octotiger
module load hpx/local
module switch --force lci lci/local-release-pcounter
