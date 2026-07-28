import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
import os
import base64
from datetime import datetime

st.set_page_config(
    page_title="Retail Intelligence Planner",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "proxima_aba" in st.session_state and st.session_state["proxima_aba"] is not None:
    st.session_state["aba_ativa"] = st.session_state["proxima_aba"]
    st.session_state["menu_navegacao_principal"] = st.session_state["proxima_aba"]
    st.session_state["proxima_aba"] = None

if "aba_ativa" not in st.session_state:
    st.session_state["aba_ativa"] = "Início"

if "menu_navegacao_principal" not in st.session_state:
    st.session_state["menu_navegacao_principal"] = "Início"

if "arquivo_carregado" not in st.session_state:
    st.session_state["arquivo_carregado"] = False

if "arquivo_usuario" not in st.session_state:
    st.session_state["arquivo_usuario"] = None

if "df_usuario" not in st.session_state:
    st.session_state["df_usuario"] = None

try:
    if st.query_params.get("ir") == "processamento":
        st.session_state["proxima_aba"] = "Processamento em Lote"
        st.query_params.clear()
        st.rerun()
except Exception:
    pass

@st.cache_data
def obter_video_base64():
    caminhos_possiveis = ["background.mp4", "background"]
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            try:
                with open(caminho, "rb") as f:
                    dados = f.read()
                return f"data:video/mp4;base64,{base64.b64encode(dados).decode()}"
            except Exception:
                pass
    return "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-and-numbers-31948-large.mp4"

video_src = obter_video_base64()

def formatar_inteiro(valor):
    return f"{int(valor):,}".replace(",", ".")

def formatar_moeda(valor):
    partes = f"{valor:,.2f}".split(".")
    milhares = partes[0].replace(",", ".")
    centavos = partes[1]
    return f"R$ {milhares},{centavos}"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html {{
        scroll-behavior: smooth;
    }}
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: #050505 !important;
        background-image: radial-gradient(circle at 50% -20%, rgba(255, 255, 255, 0.03) 0%, transparent 70%),
                          radial-gradient(circle at 80% 80%, rgba(0, 255, 170, 0.01) 0%, transparent 50%);
        color: #d4d4d8;
    }}

    /* Ocultar elementos padrao do Streamlit */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    
    /* Header Fixo Unificado */
    div[data-testid="stHorizontalBlock"]:has(.nav-logo-container) {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 70px !important;
        background: rgba(11, 12, 14, 0.92) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        z-index: 999999 !important;
        padding: 0 40px !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }}

    .navbar-brand {{
        font-weight: 700;
        font-size: 20px;
        color: #ffffff !important;
        text-decoration: none !important;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .navbar-brand span {{
        color: #00ffaa;
    }}

    .block-container {{
        padding-top: 100px !important;
    }}

    /* Ocultacao cirurgica dos marcadores de radio */
    div[role="radiogroup"] {{
        gap: 8px !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
    }}
    
    div[role="radiogroup"] [data-testid="stRadioIndicator"],
    div[role="radiogroup"] label input,
    div[role="radiogroup"] label circle,
    div[role="radiogroup"] label svg {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    div[role="radiogroup"] label > div:first-child:not(:has(span)):not(:has(p)) {{
        display: none !important;
    }}
    
    /* Estilizacao das abas de navegacao */
    div[role="radiogroup"] label {{
        background-color: transparent !important;
        border: 1px solid transparent !important;
        padding: 8px 18px !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        transition: all 0.2s ease-in-out !important;
        color: #a3a3a3 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }}
    
    div[role="radiogroup"] label:hover {{
        background-color: rgba(255, 255, 255, 0.06) !important;
        color: #ffffff !important;
    }}
    
    div[role="radiogroup"] label:has(input:checked),
    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: rgba(255, 255, 255, 0.18) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #00ffaa !important;
    }}

    /* VIDEO HERO EM TELA CHEIA (FULL-BLEED) */
    .video-hero-container {{
        position: relative;
        width: 100vw !important;
        margin-left: calc(-50vw + 50%) !important;
        height: 100vh !important;
        min-height: 550px;
        overflow: hidden;
        border-radius: 0px !important;
        margin-top: -100px !important;
        margin-bottom: 0px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .video-hero-bg {{
        position: absolute;
        top: 50%;
        left: 50%;
        min-width: 100%;
        min-height: 100%;
        width: auto;
        height: auto;
        transform: translate(-50%, -50%);
        z-index: 0;
        object-fit: cover;
    }}

    .video-hero-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, rgba(5,5,5,0.3) 0%, rgba(5,5,5,0.95) 100%);
        z-index: 1;
    }}

    .video-hero-content {{
        position: absolute;
        bottom: 18%;
        left: 8%;
        right: 8%;
        z-index: 2;
        max-width: 800px;
    }}

    .hero-title {{
        font-size: 38px;
        font-weight: 700;
        letter-spacing: -1.2px;
        line-height: 1.25;
        color: #ffffff;
        margin-bottom: 12px;
    }}

    .hero-subtitle {{
        font-size: 16px;
        color: #a3a3a3;
        margin-bottom: 0;
        line-height: 1.6;
    }}

    .hero-buttons-wrapper {{
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        margin-top: 24px;
        align-items: center;
        z-index: 2;
    }}

    .hero-primary-link {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #ffffff;
        color: #000000 !important;
        border-radius: 999px;
        padding: 10px 24px;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.6px;
        font-size: 12px;
        text-decoration: none;
        transition: all 0.2s ease-in-out;
    }}

    .hero-primary-link:link,
    .hero-primary-link:visited {{
        color: #000000 !important;
    }}

    .hero-primary-link:hover {{
        background: #00ffaa !important;
        color: #000000 !important;
        transform: translateY(-1px);
    }}

    .hero-secondary-link {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        min-height: 42px;
        padding: 0 24px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.22);
        color: #ffffff !important;
        background: rgba(255,255,255,0.04);
        text-decoration: none;
        transition: all 0.2s ease-in-out;
        font-weight: 600;
        font-size: 12px;
    }}

    .hero-secondary-link:link,
    .hero-secondary-link:visited {{
        color: #ffffff !important;
    }}

    .hero-secondary-link:hover {{
        background: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
        border-color: rgba(255,255,255,0.35);
        transform: translateY(-1px);
    }}

    /* FAIXA 1: O NUCLEO DA PLATAFORMA (BRANCA / DESTAQUE CLARO) */
    .section-info-white {{
        background: #ffffff;
        border-top: 1px solid #e4e4e7;
        border-bottom: 1px solid #e4e4e7;
        border-radius: 0px !important;
        width: 100vw !important;
        margin-left: calc(-50vw + 50%) !important;
        padding: 60px 8vw !important;
        margin-bottom: 0px !important;
        color: #111827;
    }}

    .section-info-white h2 {{
        color: #111827;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    .section-info-white p.section-intro {{
        color: #4b5563;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 36px;
        max-width: 850px;
    }}

    /* Grid de Passos de Uso no Fundo Claro */
    .steps-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }}

    .step-card-light {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        transition: all 0.25s ease;
    }}

    .step-card-light:hover {{
        border-color: #00b377;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }}

    .step-number-light {{
        display: inline-block;
        font-size: 11px;
        font-weight: 700;
        color: #007a52;
        background: rgba(0, 255, 170, 0.15);
        border: 1px solid rgba(0, 168, 112, 0.25);
        padding: 4px 10px;
        border-radius: 999px;
        margin-bottom: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .step-card-light h3 {{
        color: #0f172a;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    .step-card-light p {{
        color: #475569;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 0;
    }}

    /* FAIXA 2: EXEMPLO DO FLUXO DE TRABALHO (ESCURA / FLUINDO PARA A SIMULACAO) */
    .section-example-dark {{
        background: #0b0c0e;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0px !important;
        width: 100vw !important;
        margin-left: calc(-50vw + 50%) !important;
        padding: 56px 8vw !important;
        margin-bottom: 40px !important;
        color: #d4d4d8;
    }}

    .section-example-dark h2 {{
        color: #ffffff;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .section-example-dark p {{
        color: #a1a1aa;
        font-size: 15px;
        line-height: 1.7;
    }}

    /* Cards e Tabelas */
    .glass-card {{
        background: rgba(255, 255, 255, 0.015);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
    }}

    .section-sample-table {{
        background: rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 20px;
        color: #e5e7eb;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        line-height: 1.7;
        border: 1px solid rgba(255,255,255,0.08);
    }}

    .section-sample-table table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 12px;
    }}

    .section-sample-table th,
    .section-sample-table td {{
        padding: 10px 12px;
        text-align: left;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }}

    .section-sample-table th {{
        color: #ffffff;
        font-size: 13px;
        font-weight: 700;
    }}

    .section-sample-table td {{
        color: #d4d4d8;
    }}

    .section-sample-table tr:last-child td {{
        border-bottom: none;
    }}
    
    .status-card {{
        border-radius: 4px;
        padding: 16px 20px;
        background: rgba(255, 255, 255, 0.015);
        border: 1px solid rgba(255, 255, 255, 0.04);
        margin-top: 15px;
    }}

    div[data-baseweb="select"] > div, input {{
        background-color: #0d0d0d !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 4px !important;
        color: #ffffff !important;
    }}
    
    .stButton>button {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        letter-spacing: 0.65px;
        text-transform: uppercase;
        padding: 8px 24px !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
        height: 42px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    .stButton>button:hover {{
        background-color: #00ffaa !important;
        box-shadow: 0 0 16px rgba(0, 255, 170, 0.35) !important;
        color: #000000 !important;
    }}

    .topbar-reset-wrapper .stButton>button {{
        background-color: transparent !important;
        color: #d4d4d8 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: none !important;
    }}

    .topbar-reset-wrapper .stButton>button:hover {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }}
    
    .status-safe {{
        border-left: 3px solid #00ffaa !important;
    }}
    
    .status-warning {{
        border-left: 3px solid #eab308 !important;
    }}
    
    .status-critical {{
        border-left: 3px solid #ef4444 !important;
    }}
</style>
""", unsafe_allow_html=True)

col_logo, col_nav, col_reset = st.columns([1.8, 4.4, 1.8])

with col_logo:
    st.markdown("""
    <div class="nav-logo-container">
        <a href="#" class="navbar-brand">
            ⚡ <span>Retail</span> Intelligence
        </a>
    </div>
    """, unsafe_allow_html=True)

abas_projeto = ["Início", "Processamento em Lote", "Giro & Estoque", "Metodologia IA"]

try:
    indice_atual = abas_projeto.index(st.session_state["aba_ativa"])
except ValueError:
    indice_atual = 0

def mudar_navegacao_aba():
    nova_aba = st.session_state["menu_navegacao_principal"]
    st.session_state["aba_ativa"] = nova_aba

with col_nav:
    aba_selecionada = st.radio(
        "",
        abas_projeto,
        index=indice_atual,
        key="menu_navegacao_principal",
        on_change=mudar_navegacao_aba,
        horizontal=True,
        label_visibility="collapsed"
    )

with col_reset:
    st.markdown('<div class="topbar-reset-wrapper">', unsafe_allow_html=True)
    if st.button("Novo Processamento", use_container_width=True):
        st.session_state["proxima_aba"] = "Início"
        st.session_state["arquivo_carregado"] = False
        st.session_state["arquivo_usuario"] = None
        st.session_state["df_usuario"] = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

@st.cache_resource
def carregar_modelo_e_dados():
    try:
        with open("modelo_vendas.pkl", "rb") as f:
            modelo = pickle.load(f)
        with open("colunas_modelo.pkl", "rb") as f:
            colunas = pickle.load(f)
        dados_demo = pd.read_csv("dados_vendas_varejo.csv")
        dados_demo['Data'] = pd.to_datetime(dados_demo['Data'])
        return modelo, colunas, dados_demo, True
    except Exception:
        produtos = ["Teclado Mecânico", "Mouse Gamer", "Monitor Ultrawide", "Headset Wireless"]
        datas = pd.date_range(start="2026-01-01", end="2026-07-20", freq="D")
        dados_lista = []
        for p in produtos:
            for d in datas:
                dados_lista.append({
                    "Data": d,
                    "Produto": p,
                    "Preco_Unitario": 150.0 if "Mouse" in p else 350.0,
                    "Estoque_Disponivel": np.random.randint(50, 150),
                    "Fim_De_Semana": 1 if d.weekday() >= 5 else 0,
                    "Vendas_Do_Dia": np.random.randint(10, 40)
                })
        df_fake = pd.DataFrame(dados_lista)
        from sklearn.ensemble import RandomForestRegressor
        df_dummies = pd.get_dummies(df_fake, columns=["Produto"], drop_first=False)
        df_dummies['Mes'] = df_dummies['Data'].dt.month
        df_dummies['Dia_Da_Semana'] = df_dummies['Data'].dt.dayofweek
        X_mock = df_dummies.drop(columns=["Data", "Vendas_Do_Dia"])
        y_mock = df_dummies["Vendas_Do_Dia"]
        modelo_mock = RandomForestRegressor(n_estimators=10, random_state=42).fit(X_mock, y_mock)
        return modelo_mock, list(X_mock.columns), df_fake, True

modelo, colunas_modelo, df_demo, base_pronta = carregar_modelo_e_dados()

if st.session_state["aba_ativa"] == "Início":
    
    st.markdown(f"""
    <div class="video-hero-container">
        <video class="video-hero-bg" autoplay muted loop playsinline preload="auto">
            <source src="{video_src}" type="video/mp4">
        </video>
        <div class="video-hero-overlay"></div>
        <div class="video-hero-content">
            <h1 class="hero-title">Transforme dados históricos de vendas em insights preditivos acionáveis impulsionados por IA</h1>
            <p class="hero-subtitle">Antecipe a demanda do mercado, otimize o giro operacional e elimine rupturas de estoque com nossa inteligência analítica ponta a ponta.</p>
            <div class="hero-buttons-wrapper">
                <a href="?ir=processamento" class="hero-primary-link">Iniciar Simulação</a>
                <a href="#exemplo-demonstrativo" class="hero-secondary-link">Ver Exemplo ↓</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Faixa 1: O NÚCLEO DA PLATAFORMA (BRANCA / DESTAQUE CLARO)
    st.markdown("""<div class="section-info-white">
<h2>O núcleo da plataforma</h2>
<p class="section-intro">Uma plataforma SaaS de inteligência preditiva para o varejo, construída para reduzir rupturas, otimizar estoque e gerar previsões de demanda confiáveis em segundos. Veja como utilizar a ferramenta:</p>

<div class="steps-grid">
    <div class="step-card-light">
        <span class="step-number-light">Passo 01</span>
        <h3>Simulação Individual</h3>
        <p>Nesta página inicial, ajuste variáveis pontuais como preço, estoque físico e sazonalidades para obter diagnósticos instantâneos de demanda e alertas de ruptura.</p>
    </div>
    <div class="step-card-light">
        <span class="step-number-light">Passo 02</span>
        <h3>Processamento em Lote</h3>
        <p>Na aba <strong>Processamento em Lote</strong>, faça o upload da sua planilha CSV com o histórico de inventário para calcular a demanda e faturamento projetado de toda a sua loja.</p>
    </div>
    <div class="step-card-light">
        <span class="step-number-light">Passo 03</span>
        <h3>Análise de Giro</h3>
        <p>Acesse a aba <strong>Giro & Estoque</strong> para visualizar curvas temporais interativas em Plotly, monitorar estoque médio e identificar itens de alta retenção.</p>
    </div>
    <div class="step-card-light">
        <span class="step-number-light">Passo 04</span>
        <h3>Metodologia & IA</h3>
        <p>Consulte a aba <strong>Metodologia IA</strong> para compreender os bastidores do algoritmo de Aprendizado de Máquina (Random Forest) e as fórmulas de Estoque de Segurança.</p>
    </div>
</div>
</div>""", unsafe_allow_html=True)

    # Faixa 2: EXEMPLO DO FLUXO DE TRABALHO (ESCURA / FLUINDO PARA A SIMULAÇÃO)
    st.markdown("""<div class="section-example-dark">
<h2>Exemplo do fluxo de trabalho</h2>
<p>Veja como o sistema apresenta previsões de demanda, recomendações de estoque e métricas de giro usando dados prontos. Esta seção serve como uma demonstração confortável antes de você subir seu próprio documento.</p>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div id="exemplo-demonstrativo"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='color:#ffffff; font-weight: 600; font-size: 22px; margin-bottom: 5px;'>Exemplo Demonstrativo de Vendas Unitárias</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#737373; font-size:13px; margin-bottom:25px;'>Simule abaixo o comportamento de produtos específicos sob condições variáveis.</p>", unsafe_allow_html=True)

    col_form, col_result = st.columns([1, 2.3], gap="large")
    
    with col_form:
        st.markdown("<h3 style='font-size: 15px; font-weight:600; color:#ffffff;'>Parâmetros da Simulação</h3>", unsafe_allow_html=True)
        produtos_ativos = list(df_demo['Produto'].unique())
        produto = st.selectbox("Selecione o Produto:", produtos_ativos)
        
        preco_referencia = float(df_demo[df_demo['Produto'] == produto]['Preco_Unitario'].iloc[0])
        preco_venda = st.number_input("Preço de Venda (R$):", value=preco_referencia, step=10.0)
        
        estoque_fisico = st.slider("Estoque Atual na Loja:", 0, 500, 80)
        
        dia_sazonal = st.radio("Sazonalidade (Feriado/Fim de Semana)?", ("Não", "Sim"))
        val_sazonal = 1 if dia_sazonal == "Sim" else 0
        
        st.markdown("<br>", unsafe_allow_html=True)
        calcular_unitario = st.button("Calcular Previsão", key="calc_unit", use_container_width=True)

    with col_result:
        st.markdown("<h3 style='font-size: 15px; font-weight:600; color:#ffffff;'>Resultados da Inteligência Artificial</h3>", unsafe_allow_html=True)
        
        dados_input = pd.DataFrame(0, index=[0], columns=colunas_modelo)
        dados_input["Preco_Unitario"] = preco_venda
        dados_input["Estoque_Disponivel"] = estoque_fisico
        dados_input["Fim_De_Semana"] = val_sazonal
        dados_input["Mes"] = datetime.now().month
        dados_input["Dia_Da_Semana"] = datetime.now().weekday()
        
        col_prod = f"Produto_{produto}"
        if col_prod in colunas_modelo:
            dados_input[col_prod] = 1
        
        pred_vendas = int(np.round(modelo.predict(dados_input)[0]))
        media_historica = df_demo[df_demo['Produto'] == produto]['Vendas_Do_Dia'].mean()
        estoque_seguranca = int(np.round(media_historica * 1.5))
        
        st.markdown(f"""
        <div style="display: flex; gap: 20px; margin-top: 15px; margin-bottom: 20px;">
            <div class="glass-card" style="flex: 1; text-align: left; margin-bottom: 0;">
                <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #737373; font-weight:600;">Demanda Prevista</span>
                <h2 style="color: #ffffff; margin: 5px 0 0 0; font-size: 26px; font-weight: 600;">{formatar_inteiro(pred_vendas)} <span style="font-size: 12px; color: #737373; font-weight: 400;">un.</span></h2>
            </div>
            <div class="glass-card" style="flex: 1; text-align: left; margin-bottom: 0;">
                <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #737373; font-weight:600;">Estoque de Segurança</span>
                <h2 style="color: #ffffff; margin: 5px 0 0 0; font-size: 26px; font-weight: 600;">{formatar_inteiro(estoque_seguranca)} <span style="font-size: 12px; color: #737373; font-weight: 400;">un.</span></h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        diferenca = estoque_fisico - pred_vendas
        if diferenca < 0:
            st.markdown(f"""
            <div class="status-card status-critical">
                <strong style="color: #ffffff; font-size: 14px;">Status: Ruptura Iminente</strong><br>
                <span style="font-size: 13px; color: #a3a3a3;">O volume em estoque ({estoque_fisico} un.) não cobrirá as vendas estimadas para amanhã ({pred_vendas} un.). Providencie {abs(diferenca)} unidades adicionais para suprir a demanda.</span>
            </div>
            """, unsafe_allow_html=True)
        elif estoque_fisico < estoque_seguranca:
            st.markdown(f"""
            <div class="status-card status-warning">
                <strong style="color: #ffffff; font-size: 14px;">Status: Estoque de Alerta</strong><br>
                <span style="font-size: 13px; color: #a3a3a3;">Embora atenda o giro de amanhã, seu estoque está abaixo da zona de margem recomendada ({estoque_seguranca} un.). Considere reabastecer em breve.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-card status-safe">
                <strong style="color: #ffffff; font-size: 14px;">Status: Estoque Seguro</strong><br>
                <span style="font-size: 13px; color: #a3a3a3;">O volume atualizado cobre com folga a demanda projetada pela inteligência artificial.</span>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state["aba_ativa"] == "Processamento em Lote":
    st.markdown("<h2 style='font-size:22px; font-weight:600; margin-bottom:5px; color:#ffffff;'>Otimização de Demanda & Alocação de Estoque</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #737373; font-size: 14px;'>Carregue a planilha da sua empresa para projetar a demanda diária e prever gargalos logísticos em tempo real.</p>", unsafe_allow_html=True)
    
    col_up_1, col_up_2 = st.columns([1.5, 1], gap="large")
    
    with col_up_1:
        st.markdown("<h3 style='font-size:15px; font-weight:600; color:#ffffff;'>Envio do Inventário</h3>", unsafe_allow_html=True)
        arquivo_usuario = st.file_uploader(
            "Arraste e solte o inventário de vendas (.csv) no campo abaixo:", 
            type=["csv"],
            key="uploader_arquivo"
        )
        
        if arquivo_usuario is None:
            st.markdown("""
            <div class="status-card status-warning" style="margin-bottom: 20px;">
                <strong style="color: #ffffff;">Banco de Dados de Demonstração Ativo</strong><br>
                <span style="font-size: 13px; color: #a3a3a3;">
                    Nenhum arquivo customizado foi carregado. Atualmente estamos utilizando um histórico simulado 
                    de varejo de eletrônicos para que você possa testar os recursos do sistema.
                </span>
            </div>
            """, unsafe_allow_html=True)
            df_ativo = df_demo
            st.session_state["arquivo_carregado"] = False
            st.session_state["df_usuario"] = None
        else:
            try:
                df_ativo = pd.read_csv(arquivo_usuario)
                st.success("Tabela carregada e integrada ao mecanismo de inteligência artificial com sucesso!")
                st.session_state["arquivo_carregado"] = True
                st.session_state["df_usuario"] = df_ativo.copy()
            except Exception as e:
                st.error(f"Erro na leitura dos dados: {e}")
                df_ativo = df_demo
                st.session_state["arquivo_carregado"] = False
                st.session_state["df_usuario"] = None
                
        st.markdown("---")
        st.markdown("<h3 style='font-size:14px; font-weight:600; color:#ffffff;'>Estrutura Requerida de Colunas</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-sample-table">
            <table>
                <thead>
                    <tr><th>Data</th><th>Produto</th><th>Preco_Unitario</th><th>Estoque_Disponivel</th><th>Fim_De_Semana</th></tr>
                </thead>
                <tbody>
                    <tr><td>2026-07-18</td><td>Teclado Mecânico</td><td>250.00</td><td>120</td><td>1</td></tr>
                    <tr><td>2026-07-18</td><td>Mouse Gamer</td><td>150.00</td><td>80</td><td>1</td></tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_up_2:
        st.markdown("<h3 style='font-size:15px; font-weight:600; color:#ffffff;'>Processamento Analítico</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #737373; font-size: 13px;'>Clique para iniciar as predições de inteligência artificial em cima do arquivo ativo.</p>", unsafe_allow_html=True)
        
        executar_lote = st.button("Executar Previsões de Demanda", use_container_width=True)
        
        if executar_lote:
            try:
                df_proc = df_ativo.copy()
                df_proc['Data'] = pd.to_datetime(df_proc['Data'])
                df_proc['Mes'] = df_proc['Data'].dt.month
                df_proc['Dia_Da_Semana'] = df_proc['Data'].dt.dayofweek
                
                df_dummies = pd.get_dummies(df_proc, columns=["Produto"], drop_first=False)
                for col in colunas_modelo:
                    if col not in df_dummies.columns:
                        df_dummies[col] = 0
                        
                X_lote = df_dummies[colunas_modelo]
                df_proc["Previsao_IA"] = np.round(modelo.predict(X_lote)).astype(int)
                df_proc["Balanco_Estoque"] = df_proc["Estoque_Disponivel"] - df_proc["Previsao_IA"]
                st.session_state["df_usuario"] = df_proc.copy()
                st.session_state["arquivo_carregado"] = True
                
                total_estimado = df_proc["Previsao_IA"].sum()
                rupturas = len(df_proc[df_proc["Balanco_Estoque"] < 0])
                faturamento_estimado = (df_proc["Previsao_IA"] * df_proc["Preco_Unitario"]).sum()
                
                st.markdown(f"""
                <div class="glass-card" style="margin-top: 15px;">
                    <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #737373; font-weight:600;">Volume Total de Vendas Projetadas</span>
                    <h2 style="color: #ffffff; margin: 4px 0 0 0; font-size: 24px; font-weight: 600;">{formatar_inteiro(total_estimado)} <span style="font-size: 12px; color: #737373; font-weight: 400;">un.</span></h2>
                </div>
                <div class="glass-card">
                    <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #737373; font-weight:600;">Faturamento Estimado</span>
                    <h2 style="color: #00ffaa; margin: 4px 0 0 0; font-size: 24px; font-weight: 600;">{formatar_moeda(faturamento_estimado)}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                if rupturas > 0:
                    st.markdown(f"""
                    <div class="status-card status-critical">
                        <strong style="color: #ffffff; font-size: 14px;">Gargalos Logísticos Encontrados</strong><br>
                        <span style="font-size: 13px; color: #a3a3a3;">Foram identificados {rupturas} itens com alto risco de ruptura imediata em gôndola. Recomendamos conferência na aba Giro & Estoque.</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="status-card status-safe">
                        <strong style="color: #ffffff; font-size: 14px;">Cadeia de Suprimentos Conforme</strong><br>
                        <span style="font-size: 13px; color: #a3a3a3;">Não foram encontrados riscos de desabastecimento no lote analisado.</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                csv_saida = df_proc.to_csv(index=False).encode('utf-8')
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="Exportar Planilha de Resultados",
                    data=csv_saida,
                    file_name="predicoes_demanda.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Ocorreu um erro ao estruturar as previsões da planilha: {e}")

elif st.session_state["aba_ativa"] == "Giro & Estoque":
    st.markdown("<h2 style='font-size:22px; font-weight:600; margin-bottom:5px; color:#ffffff;'>Giro de Estoque & Análise Preditiva</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #737373; font-size: 14px;'>Acompanhe o giro real e o saldo de estoque do seu arquivo carregado. Faça upload para ativar métricas específicas do seu negócio.</p>", unsafe_allow_html=True)

    if not st.session_state.get("arquivo_carregado") or st.session_state.get("df_usuario") is None:
        st.markdown("""
        <div class="status-card status-warning" style="margin-top: 20px;">
            <strong style="color: #ffffff; font-size: 14px;">Envie um documento para ativar o Giro & Estoque</strong><br>
            <span style="font-size: 13px; color: #a3a3a3;">Faça upload do seu inventário na aba de Processamento em Lote para visualizar giro, estoque e riscos logísticos do seu próprio arquivo.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        df_usuario = st.session_state["df_usuario"].copy()
        try:
            df_usuario['Data'] = pd.to_datetime(df_usuario['Data'])
        except Exception:
            pass

        produtos_usuario = list(df_usuario['Produto'].unique()) if 'Produto' in df_usuario.columns else []
        produto_hist = st.selectbox("Selecione o Produto para Análise Cronológica:", produtos_usuario)
        df_grafico = df_usuario[df_usuario['Produto'] == produto_hist].sort_values(by="Data") if produto_hist else df_usuario

        fig = px.line(
            df_grafico,
            x="Data",
            y="Vendas_Do_Dia" if 'Vendas_Do_Dia' in df_grafico.columns else df_grafico.columns[0],
            title=f"Estudo Histórico - {produto_hist}",
            labels={"Vendas_Do_Dia": "Vendas Diárias", "Data": "Cronologia"},
            line_shape="spline"
        )

        fig.update_traces(line_color="#00ffaa", line_width=2)
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#a3a3a3",
            title_font_color="#ffffff",
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)")
        )

        st.plotly_chart(fig, use_container_width=True)

        vendas_totais = int(df_grafico['Vendas_Do_Dia'].sum()) if 'Vendas_Do_Dia' in df_grafico.columns else 0
        estoque_medio = int(df_grafico['Estoque_Disponivel'].mean()) if 'Estoque_Disponivel' in df_grafico.columns else 0
        saldo_atual = int(df_grafico['Estoque_Disponivel'].iloc[-1]) if 'Estoque_Disponivel' in df_grafico.columns else 0

        st.markdown(f"""
        <div style="display: flex; gap: 20px; margin-top: 15px;">
            <div class="glass-card" style="flex: 1;">
                <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #737373; font-weight:600;">Volume Histórico Comercializado</span>
                <h3 style="color: #ffffff; margin: 5px 0 0 0; font-size: 22px; font-weight: 500;">{formatar_inteiro(vendas_totais)} <span style="font-size: 12px; color: #737373; font-weight: 400;">un.</span></h3>
            </div>
            <div class="glass-card" style="flex: 1;">
                <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #737373; font-weight:600;">Estoque Médio Disponível</span>
                <h3 style="color: #ffffff; margin: 5px 0 0 0; font-size: 22px; font-weight: 500;">{formatar_inteiro(estoque_medio)} <span style="font-size: 12px; color: #737373; font-weight: 400;">un.</span></h3>
            </div>
            <div class="glass-card" style="flex: 1;">
                <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #737373; font-weight:600;">Saldo Atual de Estoque</span>
                <h3 style="color: #ffffff; margin: 5px 0 0 0; font-size: 22px; font-weight: 500;">{formatar_inteiro(saldo_atual)} <span style="font-size: 12px; color: #737373; font-weight: 400;">un.</span></h3>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state["aba_ativa"] == "Metodologia IA":
    st.markdown("<h2 style='font-size:22px; font-weight:600; margin-bottom:5px; color:#ffffff;'>Metodologia Científica & Algoritmo de IA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #737373; font-size: 14px;'>Saiba como a Inteligência de Negócio calcula as métricas logísticas do sistema.</p>", unsafe_allow_html=True)
    
    col_met_1, col_met_2 = st.columns(2, gap="large")
    
    with col_met_1:
        st.markdown("<h3 style='font-size:15px; font-weight:600; color:#ffffff;'>Algoritmo de Previsão de Demanda</h3>", unsafe_allow_html=True)
        st.write("""
        Utilizamos o algoritmo **Random Forest Regressor** (Floresta de Decisão Aleatória) para realizar as predições.
        Este modelo cria uma infinidade de árvores de decisão individuais durante o processo de treino, combinando 
        suas respostas para obter uma média de predição de altíssima robustez e evitar problemas comuns de sobreajuste (overfitting).
        
        As variáveis de entrada processadas (Feature Engineering) incluem:
        - **Preço de Venda do Item**: Impacta na elasticidade da demanda.
        - **Estoque Comercial Disponível**: Permite validar gargalos de disponibilidade.
        - **Dia da Semana & Mês**: Mapeiam comportamentos de sazonalidades comerciais cíclicas.
        - **Sazonalidades Críticas**: Variáveis binárias indicando datas especiais de grande fluxo.
        """)

    with col_met_2:
        st.markdown("<h3 style='font-size:15px; font-weight:600; color:#ffffff;'>Métricas Logísticas e de Suprimento</h3>", unsafe_allow_html=True)
        st.write("""
        O cálculo do **Estoque de Segurança (ES)** é um dos pilares mais tradicionais da administração de suprimentos. 
        Ele garante que, mesmo diante de variações imprevistas nos tempos de entrega dos fornecedores ou picos repentinos 
        de procura, o varejista não sofra com rupturas.
        
        A fórmula de contingenciamento applied na interface calcula o estoque de segurança dinâmico da seguinte forma:
        """)
        
        st.latex(r"ES = V_{\text{média}} \times 1.5")
        
        st.write("""
        Onde $V_{\text{média}}$ é a média histórica diária de vendas do produto selecionado. O multiplicador de $1.5$ 
        representa nossa margem de resiliência logística contra variações estatísticas.
        """)