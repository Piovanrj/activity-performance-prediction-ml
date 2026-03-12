# IA de Previsão de Rendimento de Atividades

Este projeto contém o módulo de inteligência artificial desenvolvido para um protótipo de sistema de monitoramento de atividades em ambiente computacional.

O modelo utiliza métricas de tempo coletadas durante a execução de tarefas para estimar o rendimento de atividades realizadas por usuários.

O sistema original foi desenvolvido como Trabalho de Conclusão de Curso em grupo em 2023, com cada membro sendo responsável por um dos seguintes módulos principais:

• Aplicação desktop para coleta de dados.

• Aplicação web para visualização das informações.

• Módulo de machine learning para previsão de rendimento usando LSTM (este repositório).

Nesta versão, o módulo de IA foi adaptado para funcionar de forma independente, incluindo geração de dados sintéticos, treinamento e avaliação do modelo.

## Visão Geral

Este projeto implementa um pipeline completo de machine learning para previsão de rendimento de atividades com base em métricas de tempo.

O sistema inclui:

\- geração de dados sintéticos
\- treinamento de modelos LSTM
\- previsão de rendimento
\- avaliação utilizando métricas estatísticas

## Arquitetura do Sistema Original

O sistema completo funcionava da seguinte maneira:

Desktop Application
↓
Banco de Dados (MySQL / Azure)
↓
Módulo de IA
↓
Aplicação Web

A aplicação desktop era responsável por coletar métricas de uso do computador durante a execução de atividades.  

Esses dados eram armazenados em banco de dados e utilizados pelo modelo de machine learning para gerar previsões de rendimento.

As previsões geradas eram posteriormente visualizadas através da aplicação web.

## Funcionamento do Módulo de IA

O modelo utiliza métricas de tempo relacionadas à execução de atividades para estimar o rendimento obtido em cada tarefa.

Entre os dados utilizados estão:

\- Tempo esperado da atividade.
\- Tempo produtivo.
\- Tempo ocioso.

A partir dessas métricas, o modelo gera uma estimativa de rendimento da atividade executada.

Valores de rendimento são classificados da seguinte forma:

rendimento < 0.95 → abaixo do esperado  
0.95 ≤ rendimento ≤ 1.05 → esperado  
rendimento > 1.05 → acima do esperado

## Pipeline do Modelo

O funcionamento do projeto segue as seguintes etapas:

Gerador de Dados
      ↓
Treinamento do Modelo
      ↓
Modelo Treinado
      ↓
Previsão
      ↓
Avaliação de Métricas

1\. Geração de dados sintéticos para simular atividades.
2\. Treinamento do modelo de machine learning.
3\. Aplicação do modelo em novos dados.
4\. Avaliação das previsões utilizando métricas estatísticas.

## Exemplo de saída

tempo_esperado | rendimento_real | rendimento_previsto | erro_absoluto | classe_real | classe_prevista
------------------------------------------------------------------------------------------------------
12000          | 0.98            | 1.01                | 0.03          | esperado    | esperado
14500          | 0.92            | 0.95                | 0.03          | abaixo      | esperado

Os valores apresentados nos relatórios finais são arredondados para duas casas decimais utilizando a função round(), com o objetivo de melhorar a legibilidade dos resultados.

Esse arredondamento ocorre apenas na etapa de geração do relatório e não interfere no treinamento ou na avaliação do modelo.

## Métricas de Avaliação

O desempenho do modelo é avaliado utilizando as seguintes métricas:

\- MAE (Mean Absolute Error).
\- MSE (Mean Squared Error).
\- RMSE (Root Mean Squared Error).
\- R² (Coeficiente de Determinação).
\- MAPE (Mean Absolute Percentage Error).

Essas métricas permitem analisar o erro médio das previsões realizadas pelo modelo.

## Tecnologias

\- Pandas.
\- NumPy.
\- Matplotlib.
\- TensorFlow.
\- Keras.
\- Scikit-learn.
\- OpenPyXL.

## Estrutura do Repositório

data/
    Dados de treinamento e previsão

docs/
    Documentação adicional

models/
    Modelo treinado

reports/
    Métricas e resultados gerados

src/
    Scripts principais do projeto

## Como Executar o Projeto

O projeto foi desenvolvido em 2023, então para executá-lo, será necessário um ambiente virtual com Python 3.10.

Após o ambiente virtual ser criado e ativado, deve-se seguir as próximas instruções.

1\. Instalar as dependências:

pip install -r requirements.txt

2\. Gerar os dados sintéticos:

python src/gerador\_dados.py

3\. Treinar o modelo:

python src/treinamento\_modelo.py

4\. Executar a previsão:

python src/previsao\_modelo.py

## Limitações

Este projeto foi desenvolvido originalmente como um protótipo acadêmico, possuindo algumas limitações:

\- Os dados utilizados são sintéticos.
\- O sistema completo original não está incluído neste repositório.
\- O tempo máximo considerado para atividades é de 86399 segundos (23 horas, 59 minutos e 59 segundos).
\- O modelo tende a prever valores próximos da média devido à distribuição dos dados gerados.

Essas limitações não comprometem o objetivo do projeto, que é demonstrar o pipeline completo de geração de dados, treinamento e avaliação de um modelo de machine learning.

## Sobre esta versão

Este repositório preserva a implementação original desenvolvida em 2023 como parte de um Trabalho de Conclusão de Curso.

Alterações foram mantidas mínimas para preservar o comportamento original do modelo.

Uma versão futura do projeto poderá incluir melhorias arquiteturais e atualização das bibliotecas utilizadas.

## Melhorias Futuras

Possíveis evoluções para o projeto incluem:

\- Acréscimo de dados para análise e treinamento, como tipo de atividade.
\- Melhoria do gerador de dados sintéticos.
\- Integração com sistemas externos.
\- Versionamento para funcionar com as bibliotecas atuais.