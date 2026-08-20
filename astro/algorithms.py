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

