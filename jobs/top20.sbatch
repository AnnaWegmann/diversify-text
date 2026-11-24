#!/bin/bash
#SBATCH --job-name=top20
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2g.20gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail
source .venv/bin/activate
python jobs/top20.py
