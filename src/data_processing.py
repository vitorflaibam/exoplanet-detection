import os
import pandas as pd
from lightkurve import search_lightcurve
from scipy.signal import find_peaks
import numpy as np

targets = [
    ("Kepler-10", 1),
    ("Kepler-22", 1),
    ("Kepler-62", 1),
    ("Kepler-452", 1),
    ("Kepler-186", 1),
    ("KIC 10264202", 0), # controle, sem planeta confirmado
    ("KIC 9574613", 0),  # controle
    ("KIC 8462852", 0),  # controle
]



def process_target(target_name):
    try:
        lc_file = search_lightcurve(target_name, quarter=3).download()
        if lc_file is None:
            raise ValueError("Curva não encontrada")
        lc = lc_file.PDCSAP_FLUX.normalize().remove_nans().flatten(window_length=401)
        flux = lc.flux
        mean_flux = np.mean(flux)
        std_flux = np.std(flux)
        z_scores = np.abs((flux - mean_flux) / std_flux)
        mask = z_scores < 3
        lc = lc[mask]
        df = lc.to_table().to_pandas()
        #df.reset_index(inplace=True)
        # print("Colunas do DataFrame:", df.columns)
        # print("Primeiras linhas:\n", df.head())
        # if not np.issubdtype(df['time'].dtype, np.number):
        #     df['time'] = df['time'].astype(str).str.replace(' nanoseconds', '')
        #     df['time'] = pd.to_numeric(df['time'], errors='coerce')
        time = df.index
        flux = df['flux'].values
        if isinstance(time[0], pd.Timestamp):
            time = (time - time[0]) / pd.Timedelta('1 day')
            # print("Tempo:", time[:10])
            # print("Fluxo:", flux[:10])
            # print("Tempo (tipo):", type(time[0]))
        # Parâmetros ajustados para detecção de dips mais sutis, isso podeser alterado com um range maior
        peaks, _ = find_peaks(-flux, prominence=0.00001, distance=10)

        # print("Primeiras linhas do DataFrame:")
        # print(df.head())

        if len(peaks) > 1:
            diffs = np.diff(time[peaks])
            diffs = diffs[~np.isnan(diffs)]
            period = np.mean(diffs) if len(diffs) > 0 else 0

            durations = []
            for i in range(1, len(peaks)):
                if not np.isnan(time[peaks[i]]) and not np.isnan(time[peaks[i - 1]]):
                    durations.append(time[peaks[i]] - time[peaks[i - 1]])
            duration = np.mean(durations) if len(durations) > 0 else 0
        else:
            period = 0
            duration = 0
        depth = 1 - np.min(flux[peaks]) if len(peaks) > 0 else 0
        std_flux = np.std(flux)
        skew_flux = pd.Series(flux).skew()
        kurt_flux = pd.Series(flux).kurt()
        return {
            "period": period,
            "depth": depth,
            "duration": duration,
            "std_flux": std_flux,
            "skew_flux": skew_flux,
            "kurt_flux": kurt_flux
        }
    except Exception as e:
        print(f"Falha ao processar {target_name}: {e}")
        return None


def main():
    records = []
    for target_name, label in targets:
        print(f"Processando: {target_name}")
        try:
            features = process_target(target_name)
            if features is not None:
                features['is_exoplanet'] = label
                features['target_name'] = target_name
                records.append(features)
        except Exception as e:
            print(f"Falha ao processar {target_name}: {e}")
    df = pd.DataFrame(records)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/features.csv", index=False)
    print("Dataset completo salvo em data/features.csv")

if __name__ == "__main__":
    main()
