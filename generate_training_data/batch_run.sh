#!/bin/bash
#SBATCH -N1
#SBATCH -n 1
#SBATCH -p cca
#SBATCH --constraint=skylake


srun bash -c "echo $(hostname) $SLURM_PROCID && bash run_workflow.sh $1"
