# Exoplanet Detection Pipeline

Este projeto é um pipeline automatizado para detecção de exoplanetas a partir de curvas de luz públicas obtidas por missões como Kepler e TESS, feito em Python 3.11. Projeto idealizado para o Hackaton da NASA. 

## O que o projeto faz?

- **Baixa curvas de luz** de estrelas selecionadas via Lightkurve (Kepler/TESS).
- **Pré-processa os dados**, removendo outliers e normalizando o brilho.
- **Detecta possíveis trânsitos planetários** (quedas sutis de luz causadas por planetas) automaticamente usando métodos de detecção de picos no sinal.
- **Extrai features importantes** de cada alvo:
    - Profundidade média das quedas
    - Duração e período médio dos eventos
    - Estatísticas do fluxo (desvio padrão, skewness, curtose)
- **Treina e avalia um modelo de aprendizado de máquina (Random Forest)** para diferenciar curvas de luz com e sem exoplanetas, usando exemplos rotulados (positivos e negativos).
- **Gera um relatório acessível** com o resumo dos resultados para cada estrela, incluindo gráficos e probabilidades do modelo.


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
- pandas, numpy, scipy, scikit-learn, matplotlib


## Como rodar

1. Instale as dependências (`pip install -r requirements.txt`) (caso queira usar um ambiente virtual, use `python -m venv venv`)
2. Edite a lista de alvos no script (exemplo: `data_processing.py`)
3. Execute o pipeline com:

```
python main.py
```
(ou rode pela IDE)
4. Confira os resultados nos arquivos gerados em `/data` e `/models`.

***

**Obs:** O projeto é totalmente aberto à expansão e ajustes! A comunidade astronômica e de dados é muito bem-vinda para contribuir!

---
<span style="display:none">[^1][^2][^3][^4][^5]</span>

<div style="text-align: center">⁂</div>

[^1]: main.py

[^2]: ml_model.py

[^3]: feature_extraction.py

[^4]: report_generator.py

[^5]: data_processing.py

