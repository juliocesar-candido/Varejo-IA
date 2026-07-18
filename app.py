import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Configuração da página do navegador
st.set_page_config(page_title="Predição de Estoque Inteligente", page_icon="📊", layout="wide")

# Título Principal estilizado
st.title("📊 Painel de Previsão de Demanda & Estoque com IA")
st.markdown("""
Esta ferramenta utiliza um modelo de Machine Learning (**Random Forest Regressor**) para prever 
o volume de vendas diárias de produtos e auxiliar na gestão inteligente do estoque.
""")

# Carregando o modelo e as colunas salvas
@st.cache_resource # Evita recarregar o arquivo do disco toda vez que o usuário clica em algo
def carregar_modelo_salvo():
    with open("modelo_vendas.pkl", "rb") as f:
        modelo = pickle.load(f)
    with open("colunas_modelo.pkl", "rb") as f:
        colunas = pickle.load(f)
    return modelo, colunas

try:
    modelo, colunas_modelo = carregar_modelo_salvo()
    modelo_carregado = True
except FileNotFoundError:
    modelo_carregado = False
    st.error("⚠️ Erro: Arquivo do modelo não encontrado. Rode 'python treinar_modelo.py' no terminal primeiro!")

if modelo_carregado:
    # Barra Lateral para entrada de dados do usuário
    st.sidebar.header("🔧 Parâmetros de Entrada")
    
    # Lista de produtos disponíveis
    lista_produtos = ["Teclado Mecânico", "Mouse Gamer", "Monitor 144Hz", "Headset HyperX", "Cadeira Gamer"]
    produto_selecionado = st.sidebar.selectbox("Selecione o Produto:", lista_produtos)
    
    # Preços padrões associados a cada produto
    precos_dict = {
        "Teclado Mecânico": 250.00, 
        "Mouse Gamer": 150.00, 
        "Monitor 144Hz": 1200.00, 
        "Headset HyperX": 350.00, 
        "Cadeira Gamer": 900.00
    }
    
    preco_unitario = st.sidebar.number_input("Preço Unitário (R$):", value=precos_dict[produto_selecionado], min_value=0.0)
    estoque_atual = st.sidebar.slider("Estoque Disponível na Loja:", min_value=0, max_value=500, value=50)
    fim_de_semana = st.sidebar.radio("É fim de semana / feriado?", ("Não", "Sim"))
    fim_de_semana_val = 1 if fim_de_semana == "Sim" else 0

    # Layout em colunas para os resultados
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Dados Selecionados")
        dados_input = {
            "Produto": produto_selecionado,
            "Preço": f"R$ {preco_unitario:.2f}",
            "Estoque Atual": f"{estoque_atual} unidades",
            "Fim de Semana": fim_de_semana
        }
        st.write(pd.DataFrame([dados_input]))
        
        # Botão para disparar a previsão da IA
        fazer_previsao = st.button("🤖 Calcular Previsão de Demanda")

    with col2:
        st.subheader("🔮 Resultado da IA")
        if fazer_previsao:
            # 1. Criar um DataFrame com a mesma estrutura que o modelo foi treinado (com One-Hot Encoding)
            input_dados = pd.DataFrame(0, index=[0], columns=colunas_modelo)
            
            # Preenchendo as variáveis numéricas básicas
            input_dados["Preco_Unitario"] = preco_unitario
            input_dados["Estoque_Disponivel"] = estoque_atual
            input_dados["Fim_De_Semana"] = fim_de_semana_val
            
            # Ativando a coluna dummy do produto selecionado
            coluna_produto = f"Produto_{produto_selecionado}"
            if coluna_produto in colunas_modelo:
                input_dados[coluna_produto] = 1
                
            # 2. Fazer a predição usando o modelo carregado
            previsao_vendas = modelo.predict(input_dados)[0]
            vendas_estimadas = int(np.round(previsao_vendas))
            
            # Exibir métrica visual
            st.metric(label="Previsão de Vendas para Amanhã", value=f"{vendas_estimadas} unidades")
            
            # Lógica de decisão de negócios inteligente baseada no estoque disponível
            diferenca_estoque = estoque_atual - vendas_estimadas
            
            if diferenca_estoque < 0:
                st.error(f"🚨 **Risco de Ruptura de Estoque!** É provável que faltem {abs(diferenca_estoque)} unidades para atender a demanda de amanhã. Considere reabastecer imediatamente.")
            elif diferenca_estoque <= 5:
                st.warning(f"⚠️ **Atenção:** Seu estoque ficará muito baixo (restarão apenas {diferenca_estoque} unidades após o dia).")
            else:
                st.success(f"✅ **Estoque Seguro:** Você terá {diferenca_estoque} unidades restantes. Nenhuma ação urgente é necessária.")

        
        