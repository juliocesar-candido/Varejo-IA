import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

print("1. Carregando dados históricos e de vendas...")
# Lendo o arquivo CSV de vendas gerado
df = pd.read_csv("dados_vendas_varejo.csv")

# Para enriquecer o modelo, vamos extrair novas informações inteligentes a partir da data de venda
print("2. Engenharia de Recursos (Feature Engineering) avançada...")
df['Data'] = pd.to_datetime(df['Data'])
df['Mes'] = df['Data'].dt.month
df['Dia_Da_Semana'] = df['Data'].dt.dayofweek

# Transformando a variável categórica do Produto usando One-Hot Encoding
df_processado = pd.get_dummies(df, columns=["Produto"], drop_first=False)

# Definindo nossas colunas de entrada (X) e a variável preditiva alvo (y)
X = df_processado.drop(columns=["Data", "Vendas_Do_Dia"])
y = df_processado["Vendas_Do_Dia"]

# Guardando a lista de colunas para montarmos as predições de entrada estruturadas na interface Streamlit
colunas_modelo = list(X.columns)
with open("colunas_modelo.pkl", "wb") as f:
    pickle.dump(colunas_modelo, f)

print("3. Dividindo dados para avaliação e calibração...")
# Dividindo entre 80% treino e 20% teste para avaliar assertividade estatística
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("4. Treinando o modelo de Floresta Aleatória (Random Forest)...")
modelo = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
modelo.fit(X_train, y_train)

print("5. Calculando métricas de validação do cientista de dados...")
predicoes = modelo.predict(X_test)
mae = mean_absolute_error(y_test, predicoes)
r2 = r2_score(y_test, predicoes)

print(f"-> assertividade (R²): {r2:.4f}")
print(f"-> Margem média de erro absoluto (MAE): {mae:.2f} unidades")

print("6. Exportando artefatos da IA treinada...")
# Exportando o arquivo do modelo inteligente (.pkl)
with open("modelo_vendas.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("Etapa concluída! Os novos arquivos de inteligência de predição já estão prontos para rodar no app!")