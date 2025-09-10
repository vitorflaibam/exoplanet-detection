import os

import pandas as pd

REPORT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'result_report.txt')


def run():
    print("Gerando relatório...")
    try:
        os.makedirs('data', exist_ok=True)
        features = pd.read_csv("data/features.csv")
        with open(REPORT_PATH, "w") as f:
            for i, row in features.iterrows():
                label = "Exoplaneta detectado" if row['is_exoplanet'] == 1 else "Sem evidência de exoplaneta"
                f.write(f"Alvo analisado: {row['target_name']}\n")
                f.write(f"Resultado do modelo: {label}\n")
                f.write(f"Variação no brilho da estrela (desvio padrão): {row['std_flux']:.6f}\n")
                f.write(f"Assimetria do brilho (skewness): {row['skew_flux']:.3f}\n")
                f.write(f"Kurtosis do brilho: {row['kurt_flux']:.3f}\n")
                f.write(f"Profundidade média de possíveis trânsitos: {row['depth']:.3f}\n")
                f.write(f"Período estimado entre trânsitos: {row['period']:.3f}\n")
                f.write(f"Duração estimada do trânsito: {row['duration']:.3f}\n")
                f.write(f"-----------------------------\n")
        print("Relatório acessível salvo em data/result_report.txt")
    except Exception as e:
        print("Falha ao gerar relatório:", e)
