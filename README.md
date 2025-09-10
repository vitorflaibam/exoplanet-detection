# Exoplanet Detection Pipeline

Este projeto é um pipeline automatizado para detecção de exoplanetas a partir de curvas de luz públicas obtidas por missões como Kepler e TESS, feito em Python 3.11. Projeto idealizado para o Hackaton da NASA. 

## O que o projeto faz?

### Teste local:
- **Baixa curvas de luz** de estrelas selecionadas via Lightkurve (Kepler/TESS).
- **Pré-processa os dados**, removendo outliers e normalizando o brilho.
- **Detecta possíveis trânsitos planetários** (quedas sutis de luz causadas por planetas) automaticamente usando métodos de detecção de picos no sinal.
- **Extrai features importantes** de cada alvo:
    - Profundidade média das quedas
    - Duração e período médio dos eventos
    - Estatísticas do fluxo (desvio padrão, skewness, curtose)
- **Treina e avalia um modelo de aprendizado de máquina (Random Forest)** para diferenciar curvas de luz com e sem exoplanetas, usando exemplos rotulados (positivos e negativos).
- **Gera um relatório acessível** com o resumo dos resultados para cada estrela, incluindo gráficos e probabilidades do modelo.

### API:
- Análise automática de curvas de luz para detectar a presença de exoplanetas.
- Pipeline modular: coleta dados pelo `Lightkurve`, processa, extrai *features* físicas.
- Classificação via modelo de Machine Learning treinado (Random Forest).
- Integração com dados complementares (simulados) de Variações de Tempo de Trânsito (TTV) e Velocidade Radial (RV).
- Geração automatizada de relatórios interpretáveis.

## Como funciona o fluxo

1. **Defina uma lista de estrelas** de interesse no script (controle e exoplanetas conhecidos).
2. O pipeline baixa e processa automaticamente todos os dados.
3. As features extraídas alimentam o modelo de machine learning, que aprende a separar curvas suspeitas de exoplaneta das demais.
4. O resultado inclui estatísticas, probabilidades do modelo e outputs prontos para interpretação ou análise científica.

## Recursos e diferenciais

- Fácil de expandir para dezenas/centenas de alvos só mudando a lista.
- Modular: cada passo pode ser customizado, ajustando parâmetros de detecção, filtros ou modelo.
- Inclui exemplos de visualização para depuração e apresentação.
- Relatórios são pensados para cientistas e leigos, ajudando no entendimento e divulgação.


## Limitações

- **Qualidade dos dados:** Se o alvo tem poucos trânsitos no intervalo baixado (por exemplo, só um quarter), a chance do modelo não detectar eventos reais aumenta.
- **Parâmetros de detecção:** Ajustes finos podem ser necessários para missões e estrelas diferentes.
- **Base de controle:** O desempenho do modelo melhora bastante ao incrementar exemplos de estrelas sem planeta e sem variabilidade peculiar.


## Tecnologias e dependências

- Python 3.11 (melhor compatibilidade)
- lightkurve
- pandas, numpy, scipy, scikit-learn, matplotlib, fastapi (para API), joblib (serialização do modelo)


## Como rodar localmente:

1. Descomente o método "run" do ml model
2. Instale as dependências (`pip install -r requirements.txt`) (caso queira usar um ambiente virtual, use `python -m venv venv`)
3. Edite a lista de alvos no script (exemplo: `data_processing.py`)
4. Execute o pipeline com:

```
python main.py
```
(ou rode pela IDE)
4. Confira os resultados nos arquivos gerados em `/data` e `/models`.

## Como rodar API:
1. Rodar servidor API:
`uvicorn src.api_service:app --reload` na pasta src

## Uso da API

- Endpoint `/analisar_alvo` para enviar alvo e parâmetros, recebe decisão, probabilidades e relatórios.
#### Exemplo de entrada:
```json
{
  "target_name": "Kepler-10",
  "is_exoplanet": 1,
  "ttv_rv_data": {
    "ttv_values": [0.01, 0.02, -0.01],
    "rv_times": [2458000.1, 2458001.5, 2458003.0],
    "rv_values": [5.2, -3.8, 4.1],
    "rv_errors": [0.5, 0.6, 0.5]
  }
}
```
### Response:
```json
{
  "probabilidade_exoplaneta": 0.96,
  "decisao_modelo": "Classificador identificou como EXOPLANETA com alta probabilidade",
  "provas_reais": [
    "Classificador identificou como EXOPLANETA com alta probabilidade",
    "Confirmação dinâmica (RV): Compatível com planeta",
    "Análise de TTV: Consistente com planeta"
  ],
  "relatorio": ""
}
```
### AINDA NÃO IMPLEMENTADO:
- Endpoint `/analisar_curva` para upload de curvas prontas e dados TTV/RV adicionais para análise.
***

**Obs:** O projeto é totalmente aberto à expansão e ajustes! A comunidade astronômica e de dados é muito bem-vinda para contribuir!

