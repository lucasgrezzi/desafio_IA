Análise de Sentimento em Reviews de Produtos
Este projeto visa desenvolver um modelo de classificação de Machine Learning capaz de analisar reviews de produtos e classificá-las como positivas ou negativas. Como o dataset original não fornecia uma variável de sentimento, um dos principais desafios foi a criação dessa variável a partir dos dados de avaliação (review_score).

🚀 Tecnologias e Bibliotecas
Foram utilizadas as seguintes bibliotecas:

Pandas: Para manipulação e análise dos dados.

Scikit-learn: Para pré-processamento, vetorização do texto, treinamento e avaliação do modelo.

Matplotlib e Seaborn: Para visualização dos resultados.

Numpy: Para operações numéricas e estatísticas.

🧠 Metodologia
O desenvolvimento do modelo seguiu as seguintes etapas:

1. Pré-processamento e Criação da Variável Alvo
A primeira etapa foi a criação da variável alvo. Reviews com review_score entre 4 e 5 foram classificadas como positivas (1), enquanto as com notas 1 e 2 foram classificadas como negativas (0). As reviews com nota 3 (neutras) foram removidas para garantir que o modelo aprendesse com exemplos claros. Em seguida, os comentários de texto foram limpos, com a remoção de valores nulos e pontuação.

2. Engenharia de Features (Vetorização)
Para que o modelo pudesse entender o texto, usei a técnica TF-IDF (Term Frequency-Inverse Document Frequency). Essa abordagem, que é uma evolução da simples contagem de palavras, atribui um peso maior a termos que são importantes em uma review, mas raros no dataset. Essa escolha foi crucial para garantir que o modelo focasse em palavras relevantes como 'atraso' ou 'excelente', em vez de palavras comuns.

3. Treinamento e Avaliação do Modelo
Utilizei o classificador Naive Bayes Multinomial, um algoritmo robusto e eficiente para problemas de classificação de texto. A performance foi analisada com métricas como a acurácia, a matriz de confusão e o relatório de classificação. Para garantir a confiabilidade das métricas, implementei a validação cruzada com 10 folds usando o StratifiedKFold.

Resultados da Validação Cruzada: A acurácia média de 91,57% e o baixo desvio padrão (0.0051) provaram que o modelo é robusto e consistente, performando bem em diferentes subconjuntos de dados.

Análise por Classe: A matriz de confusão e o relatório de classificação revelaram que, para as reviews positivas, o modelo alcançou uma precisão de 95% e um F1-score de 0.94. Para as reviews negativas, a precisão foi de 85% e o recall de 89%, mostrando uma excelente capacidade de identificar a maioria das reclamações.

4. 🌟 Bônus: Extração de Insights de Negócio
Para ir além da classificação, usei a análise dos pesos das palavras do modelo para extrair as que mais influenciam o sentimento. Isso permite entender as razões que tornam uma review positiva ou negativa, fornecendo insights valiosos para o negócio.

Elogios: Palavras como 'ótimo', 'excelente' e 'rápido' estão geralmente relacionadas a elogios sobre a qualidade do produto ou a agilidade da entrega.

Críticas: Palavras como 'atraso', 'problema' e 'ruim' são fortes indicadores de problemas com a logística ou a qualidade. A análise mostrou que a palavra 'não' é a mais frequente entre as avaliações negativas, indicando a negação como principal forma de expressão de insatisfação.

🛠️ Como Rodar o Projeto
Clone este repositório.

Instale as dependências: pip install pandas scikit-learn matplotlib seaborn numpy.

Execute o script principal (seu_script_principal.py) para reproduzir a análise.
