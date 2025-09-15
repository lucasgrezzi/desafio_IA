# Análise de Sentimento em Reviews de Produtos

Este projeto visa desenvolver um modelo de classificação de Machine Learning capaz de analisar reviews de produtos e classificá-las como positivas ou negativas. Como o dataset original não fornecia uma variável de sentimento, um dos principais desafios foi a criação dessa variável a partir dos dados de avaliação (review_score).

---

## 🚀 Tecnologias e Bibliotecas

Foram utilizadas as seguintes bibliotecas:

* **Pandas:** Para manipulação e análise dos dados.
* **Scikit-learn:** Para pré-processamento, vetorização do texto, treinamento e avaliação do modelo.
* **Matplotlib** e **Seaborn:** Para visualização dos resultados.

---

## 🧠 Metodologia

O desenvolvimento do modelo seguiu as seguintes etapas:

### **1. Pré-processamento e Criação da Variável Alvo**

A primeira etapa foi a criação da variável alvo. Reviews com review_score entre 4 e 5 foram classificadas como positivas, enquanto as com notas 1 e 2 foram classificadas como negativas. As reviews com nota 3 (neutras) foram removidas para garantir que o modelo aprendesse com exemplos claros. Em seguida, os comentários de texto foram limpos, com a remoção de valores nulos e pontuação.

### **2. Engenharia de Features (Vetorização)**

Para que o modelo pudesse entender o texto, usei a técnica TF-IDF (Term Frequency-Inverse Document Frequency). Essa abordagem, que é uma evolução da simples contagem de palavras, atribui um peso maior a termos que são importantes em uma review, mas raros no dataset. Essa escolha foi crucial para garantir que o modelo focasse em palavras relevantes como 'atraso' ou 'excelente', em vez de palavras comuns.

### **3. Treinamento e Avaliação do Modelo**

Utilizei o classificador Regressão Logística, que é um algoritmo robusto e eficiente para problemas de classificação. O modelo foi treinado em 80% dos dados e avaliado nos 20% restantes. A performance foi analisada com métricas como a acurácia, a matriz de confusão e o relatório de classificação, que revelaram um ótimo desempenho geral. O modelo alcançou uma acurácia de 91%, com uma precisão de 95% e um F1-score de 0.94 para a classe positiva, validando sua eficácia.

### **4. 🌟 Bônus: Extração de Razões**

Para ir além da classificação, utilizei os pesos do modelo de Regressão Logística para extrair as palavras que mais influenciam o sentimento. Isso permite entender as razões que tornam uma review positiva ou negativa, fornecendo insights valiosos para o negócio.

Elogios: Palavras como 'ótimo', 'excelente' e 'rápido' geralmente estão relacionadas a elogios sobre a qualidade do produto ou a agilidade da entrega.

Críticas: Palavras como 'atraso', 'problema' e 'ruim' são fortes indicadores de problemas com a logística ou a qualidade. A análise mostrou que a palavra 'não' é a mais frequente entre as avaliações negativas, indicando a negação como principal forma de expressão de insatisfação.

---

## 🛠️ Como Rodar o Projeto

1.  Clone este repositório.
2.  Instale as dependências: `pip install pandas scikit-learn matplotlib seaborn`.
3.  Execute o script principal (`seu_script_principal.py`) para reproduzir a análise.
