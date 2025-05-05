import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Link da planilha publicada como CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv"

st.set_page_config(page_title="Triagem ESG e Financeira", layout="wide")

st.title("🧮 Triagem ESG e Financeira de Empresas")

# Etapa 1: Dados básicos
st.header("1️⃣ Dados Básicos")
nome = st.text_input("Nome da Empresa")
segmento = st.selectbox("Segmento", ["Saúde", "Educação", "Tecnologia", "Financeiro", "Outro"])
setor = st.selectbox("Setor", ["Primário", "Secundário", "Terciário"])

indicadores_basicos = []
st.subheader("Indicadores Básicos (5)")
for i in range(1, 6):
    indicadores_basicos.append(st.radio(f"Indicador Básico {i}", ["Sim", "Não"], key=f"basic_{i}") == "Sim")

# Etapa 2: Indicadores ESG (8)
st.header("2️⃣ Indicadores ESG")
indicadores_esg = []
for i in range(1, 9):
    indicadores_esg.append(st.slider(f"Indicador ESG {i}", 0, 100, 50, key=f"esg_{i}"))

# Etapa 3: Indicadores Financeiros (9)
st.header("3️⃣ Indicadores Financeiros")
indicadores_fin = []
for i in range(1, 10):
    indicadores_fin.append(st.slider(f"Indicador Financeiro {i}", 0, 100, 50, key=f"fin_{i}"))

# Cálculo dos scores
def calcular_score(valores, pesos=None):
    if not valores:
        return 0
    if pesos is None:
        return sum(valores) / len(valores)
    else:
        return sum(v * p for v, p in zip(valores, pesos)) / sum(pesos)

score_esg = calcular_score(indicadores_esg)
score_fin = calcular_score(indicadores_fin)

aprovado_basico = all(indicadores_basicos)
aprovado_esg = score_esg >= 60
aprovado_fin = score_fin >= 60
aprovado_geral = aprovado_basico and aprovado_esg and aprovado_fin

# Resultado
st.header("✅ Resultado da Avaliação")
st.markdown(f"**Score ESG:** {score_esg:.1f}")
st.markdown(f"**Score Financeiro:** {score_fin:.1f}")
st.markdown("**Status:** " + ("🟢 Aprovado" if aprovado_geral else "🔴 Reprovado"))

# Mostrar matriz ESG x Financeiro
st.header("📊 Matriz ESG x Financeiro")
try:
    df_sheet = pd.read_csv(SHEET_URL)
except:
    df_sheet = pd.DataFrame(columns=["Empresa", "Segmento", "Setor", "Score ESG", "Score Financeiro", "Aprovada"])

# Adicionar nova empresa aprovada
if aprovado_geral and nome:
    nova_linha = pd.DataFrame({
        "Empresa": [nome],
        "Segmento": [segmento],
        "Setor": [setor],
        "Score ESG": [score_esg],
        "Score Financeiro": [score_fin],
        "Aprovada": ["Sim"]
    })
    df_sheet = pd.concat([df_sheet, nova_linha], ignore_index=True)

# Exibir matriz
fig, ax = plt.subplots()
for idx, row in df_sheet.iterrows():
    color = "green" if row["Aprovada"] == "Sim" else "red"
    ax.scatter(row["Score ESG"], row["Score Financeiro"], label=row["Empresa"], color=color)
    ax.text(row["Score ESG"] + 0.5, row["Score Financeiro"], row["Empresa"], fontsize=8)

ax.axhline(60, color="gray", linestyle="--")
ax.axvline(60, color="gray", linestyle="--")
ax.set_xlabel("Score ESG")
ax.set_ylabel("Score Financeiro")
ax.set_title("Matriz ESG x Financeiro")
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
st.pyplot(fig)
