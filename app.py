import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Função para calcular o score ESG
def calcular_score_esg(respostas):
    total_score = 0
    for i, (valor, peso, faixas) in enumerate(respostas):
        for faixa in faixas:
            if faixa[0] <= valor <= faixa[1]:
                total_score += faixa[2] * peso / 100
                break
    return total_score

# Função para calcular o score financeiro
def calcular_score_financeiro(respostas):
    total_score = 0
    for i, (valor, peso, faixas) in enumerate(respostas):
        for faixa in faixas:
            if faixa[0] <= valor <= faixa[1]:
                total_score += faixa[2] * peso / 100
                break
    return total_score

# Lista de indicadores com pesos e faixas (os mesmos da sua definição)
indicadores_esg = [
    {"indicador": "Emissão de CO2 (M ton)", "peso": 15, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador": "Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 30)]},
    {"indicador": "Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(np.inf, 0, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]},
    {"indicador": "Risco Ambiental", "peso": 5, "faixas": [(0, 1, 100), (2, 3, 70), (4, 6, 50), (7, 8, 30), (9, 10, 10)]},
]

indicadores_financeiros = [
    {"indicador": "Variação da ação YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "EBITDA (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "EBITDA YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem EBITDA (%)", "peso": 5.5 , "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Posição no MERCO", "peso": 11, "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (0, np.inf, 0)]},
    {"indicador": "Participação em Índices ESG", "peso": 11, "faixas": [(0, 0, 40), (1, 1, 80), (2, np.inf, 100)]},
    {"indicador": "Lucro Líquido (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 9.99, 80), (10, 19.99, 90), (20, np.inf, 100)]},
    {"indicador": "Lucro Líquido YoY (%)", "peso": 11, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem Líquida (%)", "peso": 5.5, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
]
st.title("Triagem ESG e Financeira - Avaliação da Empresa")

# Etapa Unificada - Coleta de Dados

st.header("Dados Básicos")
perguntas_binarias = [
    "1. A empresa tem políticas de sustentabilidade?",
    "2. A empresa possui certificação ambiental?",
    "3. A empresa divulga suas metas de redução de emissão de CO2?",
    "4. A empresa adota práticas de reciclagem?",
    "5. A empresa investe em projetos sociais?"
]

respostas_binarias = []
for i, pergunta in enumerate(perguntas_binarias):
    resposta = st.radio(pergunta, options=["Sim", "Não"], key=f"pergunta_binaria_{i}")
    respostas_binarias.append(1 if resposta == "Sim" else 0)

st.header("Indicadores ESG Quantitativos")
respostas_esg = []
for indicador in indicadores_esg:
    st.subheader(indicador["indicador"])
    valor = st.number_input(f"Digite o valor para {indicador['indicador']}:", min_value=0.0, format="%.2f", key=f"esg_{indicador['indicador']}")
    respostas_esg.append((valor, indicador["peso"], indicador["faixas"]))

st.header("Indicadores Financeiros")
respostas_financeiros = []
for indicador in indicadores_financeiros:
    st.subheader(indicador["indicador"])
    valor = st.number_input(f"Digite o valor para {indicador['indicador']}:", format="%.2f", key=f"fin_{indicador['indicador']}")
    respostas_financeiros.append((valor, indicador["peso"], indicador["faixas"]))

if st.button("Calcular Resultado Final"):
    score_financeiro = calcular_score_financeiro(respostas_financeiros)
    score_esg = calcular_score_esg(respostas_esg)
    st.session_state.score_financeiro = score_financeiro
    st.session_state.score_esg = score_esg
    st.session_state.calculado = True
    st.metric("Score ESG", score_esg)
    st.metric("Score Financeiro", score_financeiro)

    if score_financeiro > 70 and score_esg > 70:
        st.success("✅ Empresa aprovada na triagem financeira.")
        st.balloons()
        st.write("### Resultado final: Empresa Aprovada 🎉")
    else:
        st.error("❌ Empresa reprovada na triagem financeira.")
        st.write("### Resultado final: Empresa Reprovada.")

# Segunda parte 

# Carregar os dados do Google Sheets
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSOYq6bgoWRTHiMvLRt8z5KnnhDNhi0uYIkfqUztEoP9HIMdvQ_fEuG8-4n67_rZXKMcC3pU9CZLfAb/pub?gid=0&single=true&output=csv"
df = pd.read_csv(url)

# Função para atribuir nota com base nas faixas
def atribuir_nota(valor, faixas):
    for faixa in faixas:
        if faixa[0] <= valor <= faixa[1]:
            return faixa[2]
    return 0  # Nota zero caso não se encaixe em nenhuma faixa

# Indicadores ESG
indicadores_esg = [
    {"indicador": "Emissão de CO2 (M ton)", "peso": 15, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador": "Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 30)]},
    {"indicador": "Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(1, 5, 40), (6, 20, 70), (21, np.inf, 100)]},
    {"indicador": "Risco Ambiental", "peso": 5, "faixas": [(0, 1, 100), (2, 3, 70), (4, 6, 50), (7, 8, 30), (9, 10, 10)]},
]

# Indicadores Financeiros
indicadores_financeiros = [
    {"indicador": "Variação da ação YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "EBITDA (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "EBITDA YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem EBITDA (%)", "peso": 5.5 , "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Posição no MERCO", "peso": 11, "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (0, np.inf, 0)]},
    {"indicador": "Participação em Índices ESG", "peso": 11, "faixas": [(0, 0, 40), (1, 1, 80), (2, np.inf, 100)]},
    {"indicador": "Lucro Líquido (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 9.99, 80), (10, 19.99, 90), (20, np.inf, 100)]},
    {"indicador": "Lucro Líquido YoY (%)", "peso": 11, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem Líquida (%)", "peso": 5.5, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
]

# Calcular notas ESG e Financeiras
def calcular_score(linha, indicadores):
    score = 0
    for item in indicadores:
        valor = linha[item["indicador"]]
        nota = atribuir_nota(valor, item["faixas"])
        score += nota * item["peso"]
    return score / sum(item["peso"] for item in indicadores)

df["score_esg"] = df.apply(lambda row: calcular_score(row, indicadores_esg), axis=1)
df["score_financeiro"] = df.apply(lambda row: calcular_score(row, indicadores_financeiros), axis=1)

# Plotar gráfico
plt.figure(figsize=(12, 8))
plt.scatter(df["score_financeiro"], df["score_esg"], s=100, c="skyblue", edgecolors='black')

# Adicionando nomes das empresas
for i, row in df.iterrows():
    plt.text(row["score_financeiro"] + 0.5, row["score_esg"] + 0.5, row["Empresas"], fontsize=9)

plt.xlabel("Score Financeiro")
plt.ylabel("Score ESG")
plt.title("Comparação ESG vs Financeiro das Empresas")
plt.grid(True)
plt.tight_layout()
plt.show()


