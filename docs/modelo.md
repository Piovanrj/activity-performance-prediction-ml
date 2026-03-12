# Explicação do Modelo

## Objetivo do modelo

O objetivo do modelo é estimar o rendimento de atividades computacionais a partir de métricas de tempo relacionadas à execução da tarefa.

O modelo não tem como objetivo substituir avaliação humana de produtividade, mas sim fornecer uma estimativa automática baseada em padrões observados nos dados.

## Definição de rendimento

O rendimento de uma atividade é calculado com base na relação entre o tempo esperado e o tempo necessário para concluir a tarefa.

Valores próximos de 1 indicam desempenho dentro do esperado.

Valores maiores que 1 indicam conclusão da tarefa em tempo menor que o esperado.

Valores menores que 1 indicam desempenho abaixo do esperado.

## Normalização dos dados

Os dados de tempo são normalizados utilizando transformação Min-Max.

Intervalo original:
0 → 86399 segundos.

Intervalo normalizado:
0 → 1.

Os dados de rendimento são normalizados utilizando a transformação Min-Max.

Intervalo original:
Definido pela fórmula 'base = tempo_esperado[x] / (tempo_conclusao[x])' durante a geração de dados.

Intervalo normalizado:
0 → 2.

Essa transformação foi escolhida para manter os valores em escala comparável durante o treinamento do modelo.

## Estrutura do modelo

Modelo 1
Entrada:
\- Tempo esperado para conclusão.

Saída:
\- Tempo de conclusão.
\- Tempo ocioso.

Modelo 2
Entrada:
\- Tempo esperado para conclusão.
\- Tempo de conclusão.
\- Tempo ocioso.

Saída:
\- Rendimento previsto.

A divisão em dois modelos foi utilizada para decompor o problema em duas etapas:

1. Usar a informação inicial, tempo esperado, e estimar os tempos intermediários da execução da atividade (conclusão e ocioso).
2. Utilizar os três tempos (esperado, conclusão e ocioso) para prever o rendimento final.

## Geração de dados sintéticos

Devido à natureza sensível dos dados reais de monitoramento de atividades, o modelo foi treinado utilizando dados gerados artificialmente.

O gerador simula diferentes padrões de execução de atividades, incluindo:

\- Tarefas concluídas dentro do tempo esperado.
\- Tarefas concluídas acima do tempo esperado.
\- Tarefas concluídas em tempo menor que o esperado.
\- Ruído humano, um valor para simular variações naturais de desempenho durante a execução de atividades.

## Salvamento do modelo

O modelo treinado é salvo utilizando o formato `.h5` (HDF5), que era o formato padrão utilizado pelo Keras no período em que o projeto foi desenvolvido (2023).

Versões mais recentes do Keras passaram a adotar o formato `.keras` como padrão. No entanto, o formato original foi mantido nesta versão para preservar a compatibilidade com o ambiente de desenvolvimento utilizado no projeto original.

## Limitações Técnicas do Protótipo

Este projeto foi desenvolvido originalmente como um protótipo acadêmico, e algumas decisões de implementação foram mantidas nesta versão para preservar o comportamento do modelo original.

Algumas limitações conhecidas incluem:

### Treinamento não temporal

Embora o modelo utilize uma arquitetura LSTM, os dados utilizados não possuem uma estrutura temporal real entre amostras.

Na prática, cada atividade é tratada como um registro independente, o que reduz o potencial da arquitetura recorrente.

Em versões futuras, o modelo poderia utilizar sequências temporais reais de atividades para explorar melhor as capacidades da LSTM.

---

### Número elevado de épocas

O treinamento utiliza um número elevado de épocas sem mecanismos de parada antecipada.

Isso pode levar a treinamento redundante após a convergência do modelo.

Uma melhoria possível seria a utilização de técnicas como Early Stopping para interromper o treinamento quando o erro de validação parar de melhorar.

---

### Ausência de salvamento do melhor modelo

O treinamento atual não implementa salvamento automático do melhor modelo durante o processo de treinamento.

Isso significa que o modelo final salvo corresponde apenas ao estado da última época.

Uma implementação futura poderia utilizar callbacks de salvamento de checkpoints para preservar automaticamente a melhor versão do modelo.

---

### Dependência de dados sintéticos

Devido à natureza sensível dos dados originais do sistema, o modelo foi treinado utilizando dados sintéticos gerados artificialmente.

Isso pode levar o modelo a aprender padrões simplificados em comparação com um ambiente real de produção.