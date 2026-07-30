# Retail Intelligence Planner — SaaS preditivo & gestão de estoque com IA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://retail-intelligence-ia.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

> 🌐 **Acesse a aplicação online pelo seguinte endereço:** [retail-intelligence-ia.streamlit.app](https://retail-intelligence-ia.streamlit.app/)

---

> **Plataforma analítica End-to-End de inteligência preditiva para varejo:** Uma solução web em Python que combina *Machine Learning* (Random Forest Regressor) e visualização de dados interativa para prever demanda de vendas, prevenir rupturas de gôndola e otimizar a cobertura de estoque em tempo real.

---

## Demonstração da plataforma

* **Simulação preditiva unitária**: Diagnóstico imediato de demanda e alertas de risco com base em variações de preço, estoque físico e sazonalidade.
* **Processamento de inventário em lote (CSV)**: Upload de planilhas de estoque com diagnóstico automático por produto, faturamento estimado, *cards* de KPI e exportação dos resultados.
* **Dashboards de giro e estoque (Plotly express)**: Gráficos temporais interativos, comparativos de estoque físico *versus* demanda e cálculo dinâmico do índice de cobertura (dias de giro).

---

## Principais funcionalidades

- [x] **Simulação de demanda em tempo real**: Cálculo sob demanda para produtos específicos com ajuste interativo de sliders e fatores de sazonalidade.
- [x] **Motor de processamento de inventário em lote**: Upload de arquivos `.csv` com retenção de sessão (`st.session_state`), identificação dos produtos em risco de desabastecimento e destaques do lote (*Campeão de Demanda* e *Maior Risco de Ruptura*).
- [x] **Indicadores logísticos automáticos**: Classificação condicional de saúde do estoque:
  - 🟢 **Estoque seguro**: Volume atual atende à demanda e supera a margem de segurança.
  - 🟡 **Alerta de reabastecimento**: Volume dentro da margem de contingência recomendada.
  - 🔴 **Ruptura iminente**: Estoque insuficiente para cobrir as vendas estimadas.
- [x] **Curvas temporais & gráficos interativos**: Integração com `Plotly Express` e `Plotly Graph Objects` com recursos de zoom, seletores e eixos unificados.
- [x] **Explicabilidade algorítmica**: Seção dedicada à metodologia científica, detalhando *Feature Engineering* do modelo e premissas do Estoque de Segurança.

---

## Tecnologias e ferramentas utilizadas

| Camada | Tecnologia / Biblioteca | Descrição |
| :--- | :--- | :--- |
| **Linguagem principal** | `Python 3.10+` | Construção de todo o pipeline preditivo, lógica de negócios e backend. |
| **Interface web & UX** | `Streamlit` + `CSS3` | Framework reativo com estilização customizada (Glassmorphism, Dark Theme, layout responsivo e cabeçalho fixo). |
| **Machine learning** | `Scikit-Learn` | Modelo *Random Forest Regressor* com validação estatística de aderência ($R^2$, $MAE$). |
| **Análise de dados** | `Pandas` & `NumPy` | Manipulação de vetores, *One-Hot Encoding* e engenharia de recursos (*features* temporais). |
| **Data Viz** | `Plotly Express` & `Graph Objects` | Gráficos interativos multi-eixo e histogramas de comparação de inventário. |
| **Persistência de IA** | `Pickle` | Serialização e carregamento dinâmico dos artefatos treinados (`.pkl`). |

---

## Arquitetura de machine learning e logística

### Algoritmo de Previsão de Demanda

O núcleo preditivo da aplicação utiliza o algoritmo **Random Forest Regressor** (Floresta de Decisão Aleatória). O modelo foi treinado em dados históricos de vendas e processa as seguintes variáveis de entrada:

1. **Preço Unitário de Venda**: Atributo contínuo que captura a elasticidade-preço da demanda.
2. **Estoque Disponível no Dia**: Restrição física de disponibilidade comercial.
3. **Sazonalidade Cíclica**: Extração de atributos temporais (`Mês` do ano e `Dia da Semana`).
4. **Sazonalidade de Pico**: Variável binária identificando fins de semana e feriados de alto movimento.
5. **Codificação Categórica**: *One-Hot Encoding* para generalização dos produtos da loja.

### Cálculo do estoque de segurança ($ES$)

Para mitigar os riscos de indisponibilidade por imprevistos na cadeia de suprimentos ou picos súbitos de procura, a plataforma aplica o cálculo dinâmico de contingência logística:

$$ES = V_{\text{média}} \times 1.5$$

Onde $V_{\text{média}}$ representa a média diária histórica de vendas do item e $1.5$ adiciona uma margem de segurança de $50\%$.

---

## Estrutura do repositório

```text
Varejo-IA/
├── app.py                      # Aplicação principal (interface streamlit + estilização CSS)
├── treinar_modelo.py           # Pipeline de engenharia de dados, treino do modelo e exportação
├── dados_vendas_varejo.csv     # Base de dados histórica simulada para testes
├── modelo_vendas.pkl           # Artefato do modelo de Machine Learning treinado
├── colunas_modelo.pkl          # Mapeamento da ordem das variáveis do modelo
├── background_otimizado.mp4    # Vídeo de fundo leve (H.264 / 30 FPS sem áudio)
├── requirements.txt            # Arquivo de dependências para deploy na nuvem
├── .gitignore                  # Arquivos ignorados pelo controle de versão
└── README.md                   # Documentação do repositório
```
---
# Como executar o projeto localmente

Pré-requisitos
Ter o Python 3.10 ou superior instalado na máquina.

## 1. Clonar o repositório
```
git clone [https://github.com/juliocesar-candido/Varejo-IA.git](https://github.com/juliocesar-candido/Varejo-IA.git)
cd Varejo-IA
```
## 2. Criar e ativar o ambiente virtual
. Windows (PowerShell):
```
python -m venv venv
  .\venv\Scripts\Activate.ps1
```

. Linux / macOS:
```
python3 -m venv venv
  source venv/bin/activate
```

## 3. Instalar as dependências
```
pip install -r requirements.txt
```

## 4. (Opcional) Re-treinar a inteligência artificial
Se desejar gerar novos artefatos do modelo a partir do dataset CSV:
```
python treinar_modelo.py
```

## 5. Executar a aplicação web (no terminal)
```
streamlit run app.py
```
Acesse o sistema no seu navegador no endereço local

---

