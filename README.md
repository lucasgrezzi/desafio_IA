# Análise de Sentimento em Reviews de Produtos com Machine Learning e GenAI

Este projeto visa desenvolver um modelo de classificação de Machine Learning capaz de analisar reviews de produtos e classificá-las como positivas ou negativas. Um desafio inicial foi a criação da variável alvo de sentimento a partir das notas de avaliação (`review_score`), já que o dataset original não a fornecia.

A implementação utiliza técnicas de processamento de linguagem natural (NLP) com **TF-IDF** e incorpora a **Inteligência Artificial Generativa (Gemini API)** para enriquecer o treinamento do modelo.

O modelo alcançou uma **acurácia de 93%** e fornece *insights* de negócio, como a identificação das principais razões (palavras-chave) por trás da satisfação e da insatisfação dos clientes.

## 🧠 Metodologia e Pipeline

O desenvolvimento do modelo seguiu as etapas de pré-processamento, engenharia de features, e treinamento, com um destaque para o uso de IA Generativa:

1. **Criação da Variável Alvo:** Definição de sentimento (Positivo/Negativo) a partir do `review_score`. Reviews com nota 3 (neutras) foram removidas para garantir o aprendizado com exemplos claros.
2. **Pré-processamento de Texto:** Os comentários foram limpos, removendo valores nulos, pontuação e convertidos para minúsculas.
3. **Engenharia de Features:** Uso do **TF-IDF** para transformar texto em dados numéricos, focando em palavras relevantes como 'atraso' ou 'excelente'.
4. **Aumento de Dados (Data Augmentation) com GenAI:** A **Gemini API** foi utilizada para gerar 10 novos exemplos de reviews positivas sintéticas, aprimorando a capacidade de generalização do modelo.
5. **Treinamento e Avaliação:** O modelo foi treinado com os dados aumentados (Regressão Logística/Naive Bayes Multinomial) e avaliado com **Validação Cruzada (10 *folds*)** para atestar sua robustez.

## 📊 Performance do Modelo

O modelo aprimorado alcançou as seguintes métricas de desempenho no conjunto de teste:

| Métrica | Negativo (0) | Positivo (1) |
| :--- | :--- | :--- |
| **Acurácia Geral** | \multicolumn{2}{|c|}{**0.93**} |
| **F1-Score** | 0.90 | 0.95 |
| **Precisão** | 0.88 | 0.96 |
| **Recall** | 0.91 | 0.94 |

* **Alta Precisão (0.96) para Positivos:** Garante que, ao prever satisfação, o modelo está correto 96% das vezes.
* **Alto Recall (0.91) para Negativos:** Indica que o modelo é muito bom em "capturar" reclamações reais, assegurando que poucas passem despercebidas.

## 🌟 Insights de Negócio

A análise dos pesos das palavras mais influentes forneceu *insights* valiosos:

* **Críticas:** A palavra **'não'** é a mais frequente entre as avaliações negativas, indicando a negação como a principal forma de expressão de insatisfação. Termos como 'atraso', 'problema' e 'defeito' também são indicadores fortes.
* **Elogios:** Palavras como 'ótimo' e 'excelente' são fortes indicadores de satisfação, refletindo a percepção positiva da maioria dos clientes.

## 🛠️ Tecnologias utilizadas

* Python;
* Pandas library;
* Scikit-learn library;
* Numpy library;
* Matplotlib e Seaborn libraries;
* Gemini API (Google Generative AI).

## ✉️ Contact

Email: [lucasgrezzi@gmail.com]
