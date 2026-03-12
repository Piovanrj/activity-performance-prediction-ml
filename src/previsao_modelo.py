import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

modelo1 = load_model("../models/modelo1_completo.h5")
modelo2 = load_model("../models/modelo2_completo.h5")

# Carregar os dados
data = pd.read_excel('../data/atividades_agendadas.xlsx')  # Substitua pelo nome do arquivo de dados

# Pré-processamento dos dados
# ... (tratar dados faltantes, normalização, criação de sequências de entrada e saída, etc.)

prev = np.zeros([len(data), 3])

# Tratamento de dados faltantes
def tratamento_faltantes(df, colunas):
    for col in colunas:
        df[col] = df[col].fillna(0)
    return df

colunas_processamento = ['tempoEsperado']

data = tratamento_faltantes(data, colunas_processamento)

# Padronização dos valores de tempo em segundos
def normalizacao(df, colunas, minTotal = 0, maxTotal = 1):
    for col in colunas:
        minimo = 0 # df[col].min()
        maximo = 86399 #df[col].max()
        df[col] = minTotal + (df[col] - minimo) * (maxTotal - minTotal) / (maximo - minimo)
    
    return df

data = normalizacao(data, colunas_processamento)

X = data['tempoEsperado'].values

prev[:,0] = X[:]

X = X.reshape(X.shape[0], 1, 1)

previsao1 = modelo1.predict(X)

prev[:,1] = previsao1[:,0]
prev[:,2] = previsao1[:,1]

previsao2 = modelo2.predict(prev)

def inversao_normalizacao(vet, minimo, maximo, minTotal = 0, maxTotal = 1):
    for l in range(len(vet)):
        # Fórmula para reverter a normalização
        vet[l] = (vet[l] - minTotal) * (maximo - minimo) / (maxTotal - minTotal) + minimo
    return vet

previsao2 = inversao_normalizacao(previsao2, 0, 2)

rendimento_real = data['rendimento'].values
rendimento_previsto = previsao2.flatten()

mae = mean_absolute_error(rendimento_real, rendimento_previsto)
mse = mean_squared_error(rendimento_real, rendimento_previsto)
rmse = np.sqrt(mse)
r2 = r2_score(rendimento_real, rendimento_previsto)

mape = np.mean(np.abs((rendimento_real - rendimento_previsto) / rendimento_real)) * 100

with open("../reports/metricas_modelo.txt", "w") as f:
    f.write("Avaliação do Modelo de Previsão de Rendimento\n")
    f.write("--------------------------------------------\n\n")

    f.write(f"MAE  : {mae:.6f}\n")
    f.write(f"MSE  : {mse:.6f}\n")
    f.write(f"RMSE : {rmse:.6f}\n")
    f.write(f"R2   : {r2:.6f}\n")
    f.write(f"MAPE : {mape:.2f}%\n")

def classificar(v):
    if v < 0.95:
        return "abaixo"
    elif v > 1.05:
        return "acima"
    else:
        return "esperado"

resultado = pd.DataFrame({
    "tempo_esperado": inversao_normalizacao(data["tempoEsperado"].values, 0, 86399).astype(int),
    "rendimento_real": rendimento_real,
    "rendimento_previsto": rendimento_previsto
})

resultado["erro_absoluto"] = abs(resultado["rendimento_real"] - resultado["rendimento_previsto"])
resultado["classe_real"] = resultado["rendimento_real"].apply(classificar)
resultado["classe_prevista"] = resultado["rendimento_previsto"].apply(classificar)

resultado = round(resultado, 2)

resultado.to_excel("../reports/resultado_previsoes.xlsx", index=False)

print("Previsões concluídas.")
print("Arquivos gerados:")
print("- Resultado_Previsões.xlsx")
print("- Métricas_Modelo.txt")