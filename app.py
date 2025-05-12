import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Função para calcular score ESG
def calcular_score_esg(respostas):
    total_score = 0
    for valor, peso, faixas in respostas:
        for faixa in faixas:
            if faixa[0] <= valor <= faixa[1]:
                total_score += faixa[2] * peso / 100
                break
    return total_score

# Função para calcular score financeiro
def calcular_score_financeiro(respostas):
    total_score = 0
    for valor, peso, faixas in respostas:
        for faixa in faixas:
            if faixa[0] <= valor <= faixa[1]:
                total_score += faixa[2] * peso / 100
                break
    return total_score

# Enviar dados ao Google Sheets
def enviar_para_google_sheets(dados_empresa, url):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(url)
    worksheet = sh.sheet1
    worksheet.append_row(dados_empresa)

# Função para carregar dados de empresas existentes
def carregar_dados_empresas(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        for coluna in df.columns[3:]:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados da planilha: {e}")
        return pd.DataFrame()

# Indicadores ESG
indicadores_esg = [
    {"indicador": "Emissão de CO2 (M ton)", "peso": 15, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador": "Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 30)]},
    {"indicador": "Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(0, 0.99, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]},
    {"indicador": "Risco Ambiental", "peso": 5, "faixas": [(0, 1, 100), (2, 3, 70), (4, 6, 50), (7, 8, 30), (9, 10, 10)]},
]

# Indicadores Financeiros
indicadores_financeiros = [
    {"indicador": "Variação da ação YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "EBITDA (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "EBITDA YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem EBITDA (%)", "peso": 5.5, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Posição no MERCO", "peso": 11, "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (101, np.inf, 0)]},
    {"indicador": "Participação em Índices ESG", "peso": 11, "faixas": [(0, 0, 40), (1, 1, 80), (2, np.inf, 100)]},
    {"indicador": "Lucro Líquido (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 9.99, 80), (10, 19.99, 90), (20, np.inf, 100)]},
    {"indicador": "Lucro Líquido YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem Líquida (%)", "peso": 5.5, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
]

# Plotar matriz interativa com dados de empresas existentes e nova empresa

def plotar_matriz_comparativa(df, nova_empresa=None):
    if df.empty:
        st.error("Dados não carregados corretamente!")
        return
    fig = px.scatter(
        df,
        x='Score ESG',
        y='Score Financeiro',
        text='Empresa',
        color='Segmento',
        title="Matriz ESG x Financeiro",
        height=600
    )
    if nova_empresa:
        fig.add_trace(go.Scatter(
            x=[nova_empresa['Score ESG']],
            y=[nova_empresa['Score Financeiro']],
            mode='markers+text',
            marker=dict(color='red', size=12),
            text=[nova_empresa['Empresa']],
            name='Nova Empresa'
        ))
    fig.update_layout(xaxis=dict(range=[0, 100]), yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig)

# Streamlit App

st.title("Triagem ESG e Financeira - Avaliação da Empresa")

# Etapa 1 - Info
st.header("Etapa 1: Informações Básicas")
nome_empresa = st.text_input("Nome da empresa:")
segmento_empresa = st.text_input("Segmento da empresa:")
setor_empresa = st.selectbox("Setor da empresa:", ["Primário", "Secundário", "Terciário"])

st.subheader("Indicadores Básicos ESG")
perguntas_binarias = [
    "A empresa tem políticas de sustentabilidade?",
    "Possui certificação ambiental?",
    "Divulga metas de emissão de CO2?",
    "Adota práticas de reciclagem?",
    "Investimentos em projetos sociais?"
]
respostas_binarias = [1 if st.radio(pergunta, ["Sim", "Não"], key=f"binaria_{i}") == "Sim" else 0
                      for i, pergunta in enumerate(perguntas_binarias)]

# Etapa 2: Indicadores ESG
st.header("Etapa 2: Indicadores ESG")
respostas_esg = [
    (
        st.number_input(indicador['indicador'], min_value=0.0, format="%.2f", key=f"esg_{i}"),
        indicador['peso'],
        indicador['faixas']
    )
    for i, indicador in enumerate(indicadores_esg)
]

# Etapa 3: Indicadores Financeiros
st.header("Etapa 3: Indicadores Financeiros")
respostas_fin = [
    (
        st.number_input(indicador['indicador'], format="%.2f", key=f"fin_{i}"),
        indicador['peso'],
        indicador['faixas']
    )
    for i, indicador in enumerate(indicadores_financeiros)
]

# Cálculo dos Scores
score_esg = calcular_score_esg(respostas_esg)
score_fin = calcular_score_financeiro(respostas_fin)


st.metric("Score ESG", f"{score_esg:.2f}")
st.metric("Score Financeiro", f"{score_fin:.2f}")
print(df_empresas.columns)
print(df_empresas.head())

# Aprovação
if score_esg > 70 and score_fin > 70:
    st.success("✅ Empresa aprovada na triagem.")
    if st.button("Salvar empresa aprovada"):
        # Extrai apenas os valores das respostas binárias (True/False ou 0/1)
        respostas_binarias_valores = [int(r) for r in respostas_binarias]

        # Monta os dados para salvar (nome, segmento, setor, respostas binárias, score ESG, score financeiro)
        
        dados_empresa = [
            nome_empresa,
            segmento_empresa,
            setor_empresa,
            *respostas_binarias_valores,
            *respostas_esg,
            *respostas_fin
        ]

        # Link da planilha
        url_sheets = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv"

        # Envia os dados
        enviar_para_google_sheets(dados_empresa, url_sheets)
else:
    st.warning("❌ Empresa não aprovada com base nos scores.")

# Visualização da matriz completa
st.header("Matriz ESG x Financeiro (Comparativo)")

# Carrega os dados da planilha
url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv"
df_empresas = carregar_dados_empresas(url_csv)

# Aqui você já tem os scores salvos, então só precisa plotar a matriz
plotar_matriz_comparativa(df_empresas)


