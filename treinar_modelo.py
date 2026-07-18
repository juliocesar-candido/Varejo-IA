import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

print("1. Carregando os dados...")
# Lendo o arquivo CSV de vendas que geramos
df = pd.read_csv("dados_vendas_varejo.csv")

print("2. Engenharia de Recursos (Feature Engineering)...")
# Como os modelos de ML só entendem números, vamos transformar a coluna de "Produto"
# em variáveis numéricas (chamado de One-Hot Encoding)
df_processado = pd.get_dummies(df, columns=["Produto"], drop_first=False)

# Vamos definir quem queremos prever (Y - Alvo) e quais dados usaremos para prever (X - Recursos)
# Queremos prever as "Vendas_Do_Dia" usando o Preço, Estoque, se é Fim de Semana e o tipo de Produto
X = df_processado.drop(columns=["Data", "Vendas_Do_Dia"])
y = df_processado["Vendas_Do_Dia"]

# Guardando o nome das colunas de X para usarmos no app do Streamlit depois
colunas_modelo = list(X.columns)
with open("colunas_modelo.pkl", "wb") as f:
    pickle.dump(colunas_modelo, f)

print("3. Dividindo os dados em Treino e Teste...")
# 80% dos dados para treinar a IA, 20% para testar se ela realmente aprendeu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("4. Treinando o modelo (Random Forest)...")
# Usaremos o algoritmo Random Forest (Floresta Aleatória), excelente para regressão e tabelas
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

print("5. Avaliando o desempenho do modelo...")
predicoes = modelo.predict(X_test)
mae = mean_absolute_error(y_test, predicoes)
r2 = r2_score(y_test, predicoes)

print(f"-> Erro Médio Absoluto (MAE): {mae:.2f} unidades de vendas")
print(f"-> Coeficiente de Determinação (R²): {r2:.2f} (Quanto mais próximo de 1.0, melhor)")

print("6. Salvando o modelo treinado...")
# Salvamos o modelo em um arquivo .pkl para que o Streamlit possa usá-lo sem treinar do zero toda vez
with open("modelo_vendas.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("Sucesso! Modelo treinado e salvo como 'modelo_vendas.pkl'!")