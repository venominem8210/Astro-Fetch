import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import lightkurve as lk
import numpy as np
from astro.algorithms import box_least_squares_search
import matplotlib.pyplot as plt



# --- Cache or Download the Light Curve ---
cache_file = "kepler10_cache.fits"

if os.path.exists(cache_file):
    print("Loading Kepler-10 from local cache...")
    lc = lk.read(cache_file)
else:
    print("Downloading Kepler-10 light curve...")
    lc = lk.search_lightcurve("Kepler-10", mission="Kepler", cadence="long").download_all().stitch()
    lc.to_fits(cache_file, overwrite=True)

# Clean up any NaN values
lc = lc.remove_nans()

# Extract time and flux as numpy arrays
time = lc.time.value
flux = lc.flux.value

# Use 300 steps instead of 2000 so it finishes in seconds!
periods = np.linspace(0.5, 60.0, 300)

print("Running BLS search...")
best_period, best_t0, max_power, powers = box_least_squares_search(time, flux, periods)

print("BLS Search Complete!")
print(f"Best Period: {best_period} days")
print(f"Best Epoch (t0): {best_t0}")
print(f"Max Power: {max_power}")

# Plotting the periodogram
plt.figure(figsize=(10, 5))
plt.plot(periods, powers, color='royalblue', lw=1)
plt.xlabel("Trial Period (days)")
plt.ylabel("BLS Power")
plt.title("Kepler-10 Periodogram Search")
plt.grid(True, alpha=0.3)
plt.show()
