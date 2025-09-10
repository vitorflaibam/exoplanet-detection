from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import numpy as np
import os
import pandas as pd

import data_processing, ml_model, report_generator

REPORT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'result_report.txt')

app = FastAPI()

class TTVRVInput(BaseModel):
    ttv_values: Optional[list[float]] = None  # lista de variações de tempo de trânsito
    rv_times: Optional[list[float]] = None    # tempos dos pontos de RV
    rv_values: Optional[list[float]] = None   # velocidades radiais [m/s]
    rv_errors: Optional[list[float]] = None   # erros de RV [m/s]

class StarRequest(BaseModel):
    target_name: str
    is_exoplanet: int  # 1=exoplaneta, 0=controle
    ttv_rv_data: Optional[TTVRVInput] = None

def mock_ttvrv_analysis(ttv_rv_data: Optional[TTVRVInput]):
    rv_confirm = None
    ttv_signal = None

    if ttv_rv_data and ttv_rv_data.rv_values is not None:
        # Se algum valor de RV mostra amplitude entre 2 e 100 m/s = plausível
        amplitude = (np.max(ttv_rv_data.rv_values) - np.min(ttv_rv_data.rv_values)) if len(ttv_rv_data.rv_values) > 0 else 0
        if 2 < amplitude < 100:
            rv_confirm = True
        else:
            rv_confirm = False
    if ttv_rv_data and ttv_rv_data.ttv_values is not None:
        # simulação: se variação dos TTV eh pequena, indica planeta
        std_ttv = np.std(ttv_rv_data.ttv_values) if len(ttv_rv_data.ttv_values) > 0 else 999
        if std_ttv < 0.05:
            ttv_signal = True
        else:
            ttv_signal = False
    return rv_confirm, ttv_signal

def full_pipeline(target_name, is_exoplanet, ttv_rv_data):
    data_processing.targets = [(target_name, is_exoplanet)]
    data_processing.main()
    features_df = pd.read_csv("data/features.csv").drop(columns=['is_exoplanet', 'target_name'])
    probas = ml_model.predict(features_df)
    os.makedirs('data', exist_ok=True)
    with open(REPORT_PATH) as f:
        result_text = f.read()
    probability = probas[0] if len(probas) > 0 else None
    # Expande para TTV/RV
    rv_confirm, ttv_signal = mock_ttvrv_analysis(ttv_rv_data)
    provas = []
    if probability and probability > 0.8:
        provas.append("Classificador identificou como EXOPLANETA com alta probabilidade")
    else:
        provas.append("Classificador considerou como inconclusivo ou improvável")

    if rv_confirm is not None:
        provas.append(f"Confirmação dinâmica (RV): {'Compatível com planeta' if rv_confirm else 'Sem suporte claro'}")
    else:
        provas.append("Dados de velocidade radial (RV) não enviados")

    if ttv_signal is not None:
        provas.append(f"Análise de TTV: {'Consistente com planeta' if ttv_signal else 'Inconclusiva ou ruído'}")
    else:
        provas.append("Dados de TTV não enviados")

    return {
        "probabilidade_exoplaneta": probability,
        "decisao_modelo": provas[0],
        "provas_reais": provas,
        "relatorio": result_text
    }


@app.post("/analisar_alvo")
def analisar_alvo(request: StarRequest):
    resultado = full_pipeline(request.target_name, request.is_exoplanet, request.ttv_rv_data)
    return resultado

## NAO IMPLEMENTADO AINDA
# @app.post("/analisar_curva/")
# def analisar_curva(
#     lightcurve: UploadFile = File(...),
#     is_exoplanet: int = Form(...),
#     ttv_values: Optional[str] = Form(None),  # string com valores separados por vírgula
#     rv_times: Optional[str] = Form(None),
#     rv_values: Optional[str] = Form(None),
#     rv_errors: Optional[str] = Form(None),
#     target_name: Optional[str] = Form(None)
# ):
#     filepath = f"data/{lightcurve.filename}"
#     with open(filepath, "wb") as buffer:
#         buffer.write(lightcurve.file.read())
#     from src.feature_extraction import extract_features
#     extract_features(filepath, "data/features.csv")
#     ml_model.run()
#     report_generator.run()
#     with open("models/probability_scores.txt") as f:
#         probas = [float(x.strip()) for x in f.readlines()]
#     os.makedirs('data', exist_ok=True)
#     with open(REPORT_PATH) as f:
#         result_text = f.read()
#     probability = probas[0] if probas else None
#
#     def parse_series(s):
#         return [float(x) for x in s.split(",")] if s else None
#     ttv_rv_data = TTVRVInput(
#         ttv_values=parse_series(ttv_values),
#         rv_times=parse_series(rv_times),
#         rv_values=parse_series(rv_values),
#         rv_errors=parse_series(rv_errors)
#     )
#     rv_confirm, ttv_signal = mock_ttvrv_analysis(ttv_rv_data)
#     provas = []
#     if probability and probability > 0.8:
#         provas.append("Classificador identificou como EXOPLANETA com alta probabilidade")
#     else:
#         provas.append("Classificador considerou como inconclusivo ou improvável")
#     if rv_confirm is not None:
#         provas.append(f"Confirmação dinâmica (RV): {'Compatível com planeta' if rv_confirm else 'Sem suporte claro'}")
#     else:
#         provas.append("Dados de RV não enviados")
#     if ttv_signal is not None:
#         provas.append(f"Análise de TTV: {'Consistente com planeta' if ttv_signal else 'Inconclusiva ou ruído'}")
#     else:
#         provas.append("Dados de TTV não enviados")
#     os.remove(filepath)
#     return {
#         "probabilidade_exoplaneta": probability,
#         "decisao_modelo": provas[0],
#         "provas_reais": provas,
#         "relatorio": result_text
#     }
