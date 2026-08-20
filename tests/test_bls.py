import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import lightkurve as lk
import numpy as np
from astro.algorithms import box_least_squares_search

print("Downloading Kepler-10 light curve...")
lc = lk.search_lightcurve("Kepler-10", mission="Kepler", cadence="long").download_all().stitch()

# Clean up any NaN values so numpy arrays match cleanly
lc = lc.remove_nans()

# Extract time and flux as numpy arrays
time = lc.time.value
flux = lc.flux.value

# Create a grid of trial periods to search over (e.g., from 0.5 days to 20 days)
periods = np.linspace(0.5, 20.0, 1000)

print("Running BLS search...")
best_period, best_t0, max_power = box_least_squares_search(time, flux, periods)

print("BLS Search Complete!")
print(f"Best Period: {best_period} days")
print(f"Best Epoch (t0): {best_t0}")
print(f"Max Power: {max_power}")
