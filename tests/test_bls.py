print("IT WORKS")
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt

# Replace 'your_module_name' with the actual name of your Python file (without the .py)
from astro.algorithms import box_least_squares_search
