import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense

# Carregar os dados
data = pd.read_excel('../data/Atividades.xlsx')  # Substitua pelo nome do arquivo de dados

# Tratamento de dados faltantes
def tratamento_faltantes(df, colunas):
    for col in colunas:
        df[col] = df[col].fillna(0)
    return df

colunas_processamento = ['tempoConclusao', 'tempoEsperado', 'tempoOcioso']
data = tratamento_faltantes(data, colunas_processamento)

# Normalização
def normalizacao(df, colunas, minTotal = 0, maxTotal = 1):
    for col in colunas:
        minimo = 0  # assumido
        maximo = 86399  # assumido
        df[col] = minTotal + (df[col] - minimo) * (maxTotal - minTotal) / (maximo - minimo)
    return df

colunas_padroniza = ['tempoConclusao', 'tempoEsperado', 'tempoOcioso']
data = normalizacao(data, colunas_padroniza)

# Extrair arrays
X = data['tempoEsperado'].values
y = data[['tempoConclusao', 'tempoOcioso']].values
k = data[['tempoEsperado', 'tempoConclusao', 'tempoOcioso']].values
z = data['rendimento'].values

# Normalização do rendimento
def normalizacao_rendimento(vet, minTotal = 0, maxTotal = 1):
    minimo = 0
    maximo = 2
    vet = vet.copy()
    for l in range(len(vet)):
        if vet[l] > 2:
            vet[l] = 2
        vet[l] = minTotal + (vet[l] - minimo) * (maxTotal - minTotal) / (maximo - minimo)
    return vet

z = normalizacao_rendimento(z)

# Reshape para LSTM: (samples, timesteps, features) 
X = X.reshape(X.shape[0], 1, 1)

# k tem 3 features; para usar LSTM precisamos convertê-lo para 3 dims:
k = k.reshape(k.shape[0], k.shape[1], 1)  # (n, 3, 1)

# Tentar carregar modelos existentes
def try_load_model(nomes):
    for nome in nomes:
        try:
            m = load_model(nome)
            print(f"Modelo carregado: {nome}")
            return m
        except Exception:
            continue
    return None

modelo1 = try_load_model(["../models/modelo1_completo.h5"])
modelo2 = try_load_model(["../models/modelo2_completo.h5"])

# Se não existirem, criar do zero 
if modelo1 is None:
    modelo1 = Sequential()
    modelo1.add(LSTM(units=60, input_shape=(1, 1)))
    modelo1.add(Dense(units=2, activation='linear'))

if modelo2 is None:
    modelo2 = Sequential()
    # input_shape corresponde a (timesteps, features) -> (3,1) no reshape
    modelo2.add(LSTM(units=50, input_shape=(k.shape[1], 1)))
    modelo2.add(Dense(units=1, activation='linear'))

# Compilar com métricas adicionais para registro
modelo1.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae', 'mse'])
modelo2.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae', 'mse'])

# Treinamento
history1 = modelo1.fit(X, y,
                      epochs=100,
                      batch_size=16,
                      shuffle=True,         # mantido para legado
                      validation_split=0.2)

history2 = modelo2.fit(k, z,
                       epochs=100,
                       batch_size=16,
                       shuffle=True,
                       validation_split=0.2)

# Apresentação das métricas finais do modelo
print("\n===== RESULTADOS MODELO 1 =====")
print("Loss final:", history1.history['loss'][-1])
print("MAE final:", history1.history['mae'][-1])
print("MSE final:", history1.history['mse'][-1])
print("Val Loss:", history1.history['val_loss'][-1])
print("Val MAE:", history1.history['val_mae'][-1])

print("\n===== RESULTADOS MODELO 2 =====")
print("Loss final:", history2.history['loss'][-1])
print("MAE final:", history2.history['mae'][-1])
print("MSE final:", history2.history['mse'][-1])
print("Val Loss:", history2.history['val_loss'][-1])
print("Val MAE:", history2.history['val_mae'][-1])

# Gráfico dos treinamentos dos modelos
plt.plot(history1.history['loss'], label='Treino')
plt.plot(history1.history['val_loss'], label='Validação')
plt.title('Treinamento Modelo 1')
plt.xlabel('Épocas')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.plot(history2.history['loss'], label='Treino')
plt.plot(history2.history['val_loss'], label='Validação')
plt.title('Treinamento Modelo 2')
plt.xlabel('Épocas')
plt.ylabel('Loss')
plt.legend()
plt.show()

# --- Salvar modelos em .h5 (formato ainda usado quando o projeto foi desenvolvido) ---
modelo1.save("../models/modelo1_completo.h5")

modelo2.save("../models/modelo2_completo.h5")

print("Treinamento finalizado. Arquivos salvos: modelo1_completo.h5, modelo2_completo.h5")