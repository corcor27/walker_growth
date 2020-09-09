#!/bin/bash --login
#$ -cwd
#SBATCH --job-name=grow_test
#SBATCH --out=grow_test.out.%J
#SBATCH --err=grow_test.err.%J
#SBATCH --mem-per-cpu=4000
#SBATCH --ntasks=1

python brightest_growth.py
