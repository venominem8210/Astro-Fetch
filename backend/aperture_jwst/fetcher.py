import pandas as pd
from astroquery.mast import Observations
import lightkurve as lk

def fetch_exoplanet_lightcurve(target_name="WASP-39b"):
    """
    Queries the MAST archive for JWST obeservations of the specified target and extracts a clean time/flux array for dashboard visualization.
    
    """
    print(f"[INFO] Connecting to MAST archive for target: {target_name}... ")

    try:
        # Search and download the light curve using Lightkurve
        search_result = lk.search_lightcurve(target_name, mission="TESS")
        if len(search_result) == 0:
            search_result = lk.search_lightcurve(f"TIC {target_name}", mission="TESS")
            
        lc = search_result[0].download()
        
        # Clean out NaN values so Chart.js doesn't crash
        lc = lc.remove_nans()
        
        print(f"[SUCCESS] Downloaded real data for {target_name}")
        return {
            "target": target_name,
            "source": "MAST / TESS (Lightkurve)",
            "total_observations": len(lc.time),
            "time": lc.time.value.tolist(),
            "flux": lc.flux.value.tolist()
        }
    except Exception as e:
        print(f"[WARNING] MAST live query encountered an issue: {e}. Using fallback simulation data.")
    # Fallback dataset if network or query fails, ensuring your dashboard always works offline/locally
    return {
        "target": target_name,
        "source": "Local Fallback Simulation",
        "total_observations": 1,
        "time": [100.1, 100.2, 100.3, 100.4, 100.5, 100.6, 100.7, 100.8, 100.9, 101.0],
        "flux": [1.0002, 0.9998, 0.9920, 0.9850, 0.9845, 0.9915, 0.9999, 1.0001, 0.9995, 1.0000]
    } 
if __name__=="__main__":
     # Test block when running fetcher.py directly
    result = fetch_exoplanet_lightcurve("WASP-39b")
    print("Test Output:", result)  




