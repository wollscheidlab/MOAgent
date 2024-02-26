#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
conda init bash
conda activate moagent
current_dir=$(dirname "$0")
chmod +x "$current_dir/MOAgent.desktop"
cd "$current_dir"
python3 MOAgent.py
