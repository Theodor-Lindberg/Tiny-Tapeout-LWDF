#!/bin/bash

# Load VS Code editor
module load prog/vscode/1.85.2

# Load Python
module load prog/anaconda3/2024.10.1

# Install cocotb for running the testbench
python -m pip install cocotb

# Load open source tools, specifically GHDL
module load prog/oss-cad-suite/2025.03.10
