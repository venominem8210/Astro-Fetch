import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt
from astro.algorithms import box_least_squares_search

print("Downloading Kepler-10 light curve...")
# Download Kepler-10 data
lc = lk.search_lightcurve("Kepler-10", mission="Kepler", cadence="long").download_all().stitch()

print("Running BLS search...")
results = box_least_squares_search(lc)

print("BLS Results found!")
print(results)
