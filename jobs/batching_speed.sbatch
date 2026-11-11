#!/bin/bash
#SBATCH --job-name=batching_speed
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2g.20gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=00:20:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail
source .venv/bin/activate
DIVERSIFY_TEST_SPEED=1 DIVERSIFY_TEST_DEVICE=cuda \
    python -m pytest tests/test_batching_speed.py -s
echo "SMOKE OK"
