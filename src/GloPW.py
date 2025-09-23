# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 14:57:51 2025

@author: 368809
"""

from pathlib import Path
import os

# Get the directory where this script is located
script_dir = Path(__file__).resolve().parent

# Change working directory
os.chdir(script_dir)

# Run Wave Occurrence Model
exec(open('wave_occurrence_model.py').read())

# Run Wave Power Model
exec(open('wave_power_model.py').read())

