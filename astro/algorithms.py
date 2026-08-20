import numpy as np
from scipy.signal import savgol_filter

def phase_fold_lightcurve(time: np.ndarray, flux: np.ndarray, period: float, t0: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    """
    Phase folds a light curve given a specific orbital period and reference transit time (t0).
    Maps time into a phased coordinate system between -0.5 and 0.5.

    """
    # Calculate phase on a continuous interval centered around the transit
    phases = ((time - t0)/period)%1.0
    phases = np.where(phases >= 0.5, phases - 1.0, phases)

    # Sort the data points by phase for clean plotting/analysis
    sort_idx = np.argsort(phases)
    return phases[sort_idx], flux[sort_idx]

def detrend_lightcurve(time: np.ndarray, flux: np.ndarray, window_length: int = 101, polyorder: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """
    Applies a Savitzky-Golay filter to remove long-term stellar trends and instrumental noise 
    from a light curve while preserving sharp transit features.
    """

    # Ensure window length is odd as required by the filter
    if window_length%2 == 0:
        window_length += 1

    # Calculate the smooth trend line
    trend = savgol_filter(flux, windoe_length=window_length, polyorder=polyorder)

    # Flatten/detrend the flux by dividing out (or subtracting) the trend
    detrended_flux = flux / trend
    
    return time, detrended_flux

def box_least_squares_search(
        time: np.ndarray,
        flux: np.ndarray,
        periods: np.ndarray,
        duration_frac: float = 0.05,
        nbins: int = 100) -> tuple[float, float, float]:
        """
        Performs a raw Box Least Squares (BLS) search over a grid of trial orbital periods
        to detect periodic transit signals in a light curve.
        """
        best_period = periods[0]
        best_t0 = time[0]
        max_power = -float('inf')
        powers = []

        # Iterate through each trial period
        for period in periods:
        # Phase fold the light curve for the current period
           phases = ((time-time[0])/period)% 1.0

        # Sort by phase
        sort_idx = np.argsort(phases)
        sorted_phases = phases[sort_idx]
        sorted_flux = flux[sort_idx]

        # Bin the phase-folded light curve to speed up box fitting
        bin_edges = np.linspace(0.0, 1.0, nbins+1)
        bin_indices = np.digitize(sorted_phases, bin_edges) - 1

        binned_flux = np.zeros(nbins)
        binned_counts = np.zeros(nbins)

        for i in range (len(sorted_flux)):
             b_idx = bin_indices[i]
             if 0<= b_idx < nbins :
                  binned_flux[b_idx] += sorted_flux[i]
                  binned_counts[b_idx] += 1

         # Avoid division by zero for empty bins
        valid_bins = binned_counts > 0
        valid_bins = binned_counts > 0
        
        # Only process if we have enough valid bins (skips the rest of this iteration if not)
        if np.sum(valid_bins) >= nbins * 0.5:
            binned_flux[valid_bins] /= binned_counts[valid_bins]

        # Test different box widths (transit durations)
        transit_bins = max(1, int(nbins * duration_frac))

        for i in range(nbins):
             # Wrap around box summing for transit duration
             box_indices = [(i+j) % nbins for j in range(transit_bins)]
             box_vals = [binned_flux[idx] for idx in box_indices if valid_bins[idx]]

             if len(box_vals) < transit_bins *0.7:
                  continue
             
             # Calculate transit depth power
             mean_out_of_box = np.mean([binned_flux[idx] for idx in range(nbins) if idx not in box_indices and valid_bins[idx]])
             mean_in_box = np.mean(box_vals)

             depth = mean_out_of_box - mean_in_box

             # Power metric: deeper transit signal relative to baseline noise
             power = depth * np.sqrt(len(box_vals))
             powers.append(power)
            
             if power > max_power:
                max_power = power
                best_period = period
                best_t0 = time[0] + (bin_edges[i] * period)
        return best_period, best_t0, max_power, np.array(powers)