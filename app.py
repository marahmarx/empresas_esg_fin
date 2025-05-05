import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Página de seleção ---
st.set_page_config(page_title="Triagem ESG e Financeira", layout="wide")
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Escolha a etapa:", ["1. Carregar dados", "2. Calcular scores", "3. Matriz ESG x Financeiro"])

# --- 1. Carregar dados das empresas ---
@st.cache_data
def carregar_dados():
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv'
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df_empresas = carregar_dados()

# --- 2. Lista de indicadores com pesos e faixas ---
indicadores = [
    {"indicador": "Política Ambiental Formalizada (1 ou 0)", "peso": 1.92, "categoria": "ESG", "faixas": [(1, 1, 100), (0, 0, 50)]},
    {"indicador": "Relatórios de Sustentabilidade Auditados", "peso": 1.92, "categoria": "ESG", "faixas": [(1, 1, 100), (0, 0, 50)]},
    {"indicador": "Práticas Anticorrupção", "peso": 1.92, "categoria": "ESG", "faixas": [(1, 1, 100), (0, 0, 40)]},
    {"indicador": "Comitê ESG Existente", "peso": 1.92, "categoria": "ESG", "faixas": [(1, 1, 100), (0, 0, 50)]},
    {"indicador": "Transparência Financeira", "peso": 1.92, "categoria": "ESG", "faixas": [(1, 1, 100), (0, 0, 40)]},
    {"indicador": "Emissão de CO2 (M ton)", "peso": 5.77, "categoria": "ESG", "faixas": [(0, 1000, 100), (1000.01, 5000, 70), (5000.01, np.inf, 40)]},
    {"indicador": "Gestão de Resíduos (%)", "peso": 5.77, "categoria": "ESG", "faixas": [(90, 100, 100), (70, 89.99, 70), (0, 69.99, 40)]},
    {"indicador": "Eficiência energética (%)", "peso": 5.77, "categoria": "ESG", "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 40)]},
    {"indicador": "Diversidade e Inclusão Mulheres (%)", "peso": 5.77, "categoria": "ESG", "faixas": [(50, 100, 100), (30, 49.99, 70), (0, 29.99, 40)]},
    {"indicador": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 5.77, "categoria": "ESG", "faixas": [(50, 100, 100), (30, 49.99, 70), (0, 29.99, 40)]},
    {"indicador": "Índice de Satisfação dos Funcionários (%)", "peso": 1.92,"categoria": "ESG", "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 40)]},
    {"indicador": "Investimento em Programas Sociais (R$ M)", "peso": 5.77,"categoria": "ESG", "faixas": [(1, np.inf, 100), (0, 0, 50)]},
    {"indicador": "Risco Ambiental - existência de riscos (0 a 10)", "peso": 3.85, "categoria": "ESG", "faixas": [(0, 0, 100), (1, 1, 50)]},
    {"indicador": "Variação da ação YoY (%)", "peso": 7.89, "categoria": "Financeiro", "faixas": [(-np.inf, 0, 0), (0.01, 10, 40), (10.01, 20, 70), (20.01, np.inf, 100)]},
    {"indicador": "EBITDA (R$ Bi)", "peso": 7.89, "categoria": "Financeiro", "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "EBITDA YoY (%)", "peso": 5.26, "categoria": "Financeiro", "faixas": [(-np.inf, 0, 0), (0, 9.99, 40), (10, 14.99, 70), (15, np.inf, 100)]},
    {"indicador": "Margem EBITDA (%)", "peso": 2.63, "categoria": "Financeiro", "faixas": [(-np.inf, 0, 0), (0, 9.99, 40), (10, 19.99, 70), (20, np.inf, 100)]},
    {"indicador": "Posição no MERCO", "peso": 5.26, "categoria": "Financeiro", "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (101, np.inf, 0)]},
    {"indicador": "Participação em Índices ESG (quantidade)", "peso": 5.26, "categoria": "Financeiro", "faixas": [(0, 0, 40), (1, 1, 70), (2, np.inf, 100)]},
    {"indicador": "Lucro Líquido (R$ Bi)", "peso": 7.89, "categoria": "Financeiro", "faixas": [(-np.inf, 0, 0), (0, 9.99, 40), (10, 19.99, 70), (20, np.inf, 100)]},
    {"indicador": "Lucro Líquido YoY (%)", "peso": 5.26, "categoria": "Financeiro", "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "Margem Líquida (%)", "peso": 2.63, "categoria": "Financeiro", "faixas": [(-np.inf, 0, 0), (0, 9.99, 40), (10, 19.99, 70), (20, np.inf, 100)]},
]

def tratar_dados(df):
    for indicador in [i["indicador"] for i in indicadores]:
        if indicador in df.columns:
            df[indicador] = (
                df[indicador]
                .astype(str)
                .str.replace(',', '.', regex=False)
                .str.extract(r'([-+]?\d*\.?\d+)')[0]
                .astype(float)
                .fillna(0)
            )
    return df

def calcular_pontuacao(valor, faixas):
    for minimo, maximo, nota in faixas:
        if minimo <= valor <= maximo:
            return nota
    return 0

def calcular_scores(df):
    df = tratar_dados(df)
    dados_empresas = []

    peso_esg_total = sum(i["peso"] for i in indicadores if i["categoria"].lower() == "esg")
    peso_fin_total = sum(i["peso"] for i in indicadores if i["categoria"].lower() == "financeiro")

    for _, empresa in df.iterrows():
        score_esg = 0
        score_fin = 0

        for indicador_info in indicadores:
            nome = indicador_info["indicador"]
            valor = empresa.get(nome, 0)
            nota = calcular_pontuacao(valor, indicador_info["faixas"])
            score_ponderado = nota * indicador_info["peso"] / 100

            if indicador_info["categoria"].lower() == "esg":
                score_esg += score_ponderado
            else:
                score_fin += score_ponderado

        score_esg_normalizado = score_esg * (100 / peso_esg_total)
        score_fin_normalizado = score_fin * (100 / peso_fin_total)
        score_final = (score_esg_normalizado + score_fin_normalizado) / 2

        dados_empresas.append({
            "Empresas": empresa["Empresas"],
            "Score ESG": score_esg_normalizado,
            "Score Financeiro": score_fin_normalizado,
            "Score Final": score_final
        })

    return pd.DataFrame(dados_empresas)
