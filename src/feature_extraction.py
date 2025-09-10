import pandas as pd
import numpy as np
from scipy.signal import find_peaks


def extract_features(lightcurve_csv, out_csv):
    df = pd.read_csv(lightcurve_csv)
    time = df['time'].values
    flux = df['flux'].values

    peaks, props = find_peaks(-flux, height=0.98, distance=100)
    if len(peaks) > 1:
        period = np.mean(np.diff(time[peaks]))
    else:
        period = 0

    depth = np.mean(flux[peaks]) if len(peaks) > 0 else 0

    duration = np.mean([(time[i] - time[i - 1]) for i in peaks[1:]]) if len(peaks) > 1 else 0

    std_flux = np.std(flux)
    skew_flux = pd.Series(flux).skew()
    kurt_flux = pd.Series(flux).kurt()

    data = {
        "period": [period],
        "depth": [depth],
        "duration": [duration],
        "std_flux": [std_flux],
        "skew_flux": [skew_flux],
        "kurt_flux": [kurt_flux]
    }
    features_df = pd.DataFrame(data)
    features_df['is_exoplanet'] = 1
    features_df.to_csv(out_csv, index=False)

    print(f"Features extraídas e salvas em {out_csv}")
