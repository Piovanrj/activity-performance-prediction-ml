import pandas as pd
import numpy as np
import random as rd

# Quantidade de dados a serem gerados
qtd = 3100

# Quantidade de dados separada para a previsão
agendados = 100

col = 'tempoEsperado tempoConclusao tempoOcioso rendimento'.split()

tempo_esperado = np.random.normal(loc=14400, scale=14400, size=qtd)

# Limitar intervalo entre 1h e 8h
tempo_esperado = np.clip(tempo_esperado, 3600, 28800).astype(int)

tempo_conclusao = np.zeros(qtd)

tempo_ocioso = np.zeros(qtd)

rendimento = np.zeros(qtd)

resultado = np.zeros([qtd, 4])

for x in range (qtd):

    # Analise do tempo ocioso
    prob_ocioso = rd.random()

    # Normalmente o tempo ocioso tende a 0, fora pausas longas
    if prob_ocioso < 0.6:
        tempo_ocioso[x] = 0
    else:
        tempo_ocioso[x] = abs(np.random.normal(300,200))
        tempo_ocioso[x] = min(tempo_ocioso[x], 1800).astype(int)

     # Desempenho do colaborador
    prob = rd.random()

    if prob < 0.5:
        # Maioria termina próximo do esperado
        tempo_conclusao[x] = tempo_esperado[x] + rd.randint(-1800,1800)

    elif prob < 0.75:
        # Alguns demoram mais
        tempo_conclusao[x] = tempo_esperado[x] + rd.randint(900,7200)

    else:
        # Poucos terminam muito rápido
        tempo_conclusao[x] = tempo_esperado[x] - rd.randint(900,5400)

    # Evitar tempos irreais
    tempo_conclusao[x] = max(1800, tempo_conclusao[x])

    # Cálculo de rendimento
    base = tempo_esperado[x] / (tempo_conclusao[x])

    # Adicionar ruído humano
    ruido = np.random.normal(0,0.1)

    rendimento[x] = base + ruido

    # Limitar intervalo
    rendimento[x] = max(0, min(2, rendimento[x]))

resultado = np.column_stack((tempo_esperado, tempo_conclusao, tempo_ocioso, rendimento))

dados_atividades = pd.DataFrame(resultado[:qtd-agendados], columns=col)

dados_agendados = pd.DataFrame(resultado[qtd-agendados:], columns=col)

dados_atividades.to_excel("../data/atividades.xlsx", index=False)

dados_agendados.to_excel("../data/atividades_agendadas.xlsx", index=False)