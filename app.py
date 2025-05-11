import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from google.oauth2.service_account import Credentials
from gsheets_streamlit import GSheetsConnection
import gspread

# Estabelece a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê os dados da planilha
df = conn.read(
    spreadsheet="https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv",
    worksheet="Indicadores"  
)


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
def enviar_para_google_sheets(dados_empresa, sheet_url, aba_nome="Indicadores"):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )
        client = gspread.authorize(credentials)
        planilha = client.open_by_url(sheet_url)
        aba = planilha.worksheet(aba_nome)
        aba.append_row(dados_empresa, value_input_option="USER_ENTERED")
        st.success("Empresa adicionada ao Google Sheets com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar no Google Sheets: {e}")

# Plotar matriz ESG x Financeiro
def plotar_matriz_interativa(df):
    fig = px.scatter(
        df,
        x="Score Financeiro",
        y="Score ESG",
        text="Empresa",
        color="Segmento",
        size_max=60,
        title="Matriz ESG x Financeiro",
        width=800,
        height=600
    )
    fig.update_traces(textposition='top center')
    fig.update_layout(xaxis=dict(range=[0, 100]), yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig)

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

# Título
st.title("Triagem ESG e Financeira - Avaliação da Empresa")

# Etapa 1 - Informações Básicas
st.header("Etapa 1: Informações Básicas")
nome_empresa = st.text_input("Nome da empresa:")
segmento_empresa = st.text_input("Segmento da empresa:")
setor_empresa = st.selectbox("Setor da empresa:", ["Primário", "Secundário", "Terciário"])

# Etapa 1 - Perguntas Sim/Não
st.subheader("Indicadores Básicos ESG")
perguntas_binarias = [
    "A empresa tem políticas de sustentabilidade?",
    "Possui certificação ambiental?",
    "Divulga metas de emissão de CO2?",
    "Adota práticas de reciclagem?",
    "Investimentos em projetos sociais?"
]
respostas_binarias = []
for i, pergunta in enumerate(perguntas_binarias):
    resposta = st.radio(pergunta, ["Sim", "Não"], key=f"binaria_{i}")
    respostas_binarias.append(1 if resposta == "Sim" else 0)

# Etapa 2 - ESG Quantitativo
st.header("Etapa 2: Indicadores ESG")
respostas_esg = []
for indicador in indicadores_esg:
    valor = st.number_input(f"{indicador['indicador']}:", min_value=0.0, format="%.2f", key=f"esg_{indicador['indicador']}")
    respostas_esg.append((valor, indicador["peso"], indicador["faixas"]))

# Etapa 3 - Financeiro
st.header("Etapa 3: Indicadores Financeiros")
respostas_financeiras = []
for indicador in indicadores_financeiros:
    valor = st.number_input(f"{indicador['indicador']}:", format="%.2f", key=f"fin_{indicador['indicador']}")
    respostas_financeiras.append((valor, indicador["peso"], indicador["faixas"]))

# Cálculo dos scores
score_esg = calcular_score_esg(respostas_esg)
score_fin = calcular_score_financeiro(respostas_financeiras)

st.metric("Score ESG", f"{score_esg:.2f}")
st.metric("Score Financeiro", f"{score_fin:.2f}")

# Aprovação e envio
if score_esg > 70 and score_fin > 70:
    st.success("✅ Empresa aprovada na triagem.")
    if st.button("Salvar empresa aprovada"):
        dados_empresa = [
            nome_empresa,
            segmento_empresa,
            setor_empresa,
            *respostas_binarias,
            round(score_esg, 2),
            round(score_fin, 2)
        ]
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv"
        enviar_para_google_sheets(dados_empresa, url)
else:
    st.warning("❌ Empresa não aprovada com base nos scores.")

# Segunda parte

# Mostrar matriz ESG x Financeiro sempre que os scores estiverem disponíveis

# Função para carregar dados sem cache
def carregar_dados_empresas(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()  # Remover espaços nas colunas
        
        # Converter as colunas para numérico (forçando erros a se tornarem NaN)
        for coluna in df.columns[3:]:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados da planilha: {e}")
        return pd.DataFrame()

# Função para aplicar faixas de pontuação
def aplicar_faixas(valor, faixas):
    for faixa in faixas:
        if faixa[0] <= valor <= faixa[1]:
            return faixa[2]
    return 0  # Pontuação padrão

# Função para calcular os scores
def calcular_scores(df):
    esg_total = []
    financeiro_total = []

    for _, row in df.iterrows():
        score_esg = 0
        score_financeiro = 0

        for indicador in indicadores_esg:
            valor = row.get(indicador["indicador"], np.nan)
            if pd.notna(valor):
                score_esg += aplicar_faixas(valor, indicador["faixas"]) * indicador["peso"] / 100

        for indicador in indicadores_financeiros:
            valor = row.get(indicador["indicador"], np.nan)
            if pd.notna(valor):
                score_financeiro += aplicar_faixas(valor, indicador["faixas"]) * indicador["peso"] / 100

        esg_total.append(score_esg)
        financeiro_total.append(score_financeiro)

    df["Score ESG"] = esg_total
    df["Score Financeiro"] = financeiro_total
    return df
        
# Função para plotar com Plotly
import plotly.graph_objects as go

def plotar_matriz_interativa(df):
    if df.empty:
        st.error("Dados não carregados corretamente!")
        return

    if 'Empresa' not in df.columns or 'Score ESG' not in df.columns or 'Score Financeiro' not in df.columns:
        st.error("As colunas necessárias ('Empresa', 'Score ESG', 'Score Financeiro') não estão presentes.")
        return

    fig = px.scatter(
        df,
        x='Score ESG',
        y='Score Financeiro',
        text='Empresa',
        color_discrete_map={'Nova Empresa': 'red', 'Empresas Existentes': 'blue'},
        title="Matriz ESG x Financeiro",
        height=600
    )

    # Mostrar os nomes das empresas sobre os pontos
    fig.update_traces(
        textposition='top center',
        mode='markers+text',  # ESSENCIAL para mostrar os nomes
        marker=dict(size=12)
    )

    # Faixas visuais
    shapes = [
    dict(type="rect", x0=0, y0=0, x1=70, y1=70, fillcolor="rgba(255, 0, 0, 0.1)", line=dict(width=0)),           # Baixo ESG e Financeiro
    dict(type="rect", x0=70, y0=0, x1=100, y1=70, fillcolor="rgba(255, 165, 0, 0.1)", line=dict(width=0)),        # ESG alto, Financeiro baixo
    dict(type="rect", x0=0, y0=70, x1=70, y1=100, fillcolor="rgba(173, 216, 230, 0.1)", line=dict(width=0)),      # ESG baixo, Financeiro alto
    dict(type="rect", x0=70, y0=70, x1=100, y1=100, fillcolor="rgba(144, 238, 144, 0.15)", line=dict(width=0)),   # ESG alto e Financeiro alto
]
    fig.update_layout(shapes=shapes)

    # Define limites dos eixos
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])

    st.plotly_chart(fig, use_container_width=True)

#Terceira Parte
# Parte principal da interface

if st.session_state.get('calculado'):
    st.header("📊 Comparativo: Matriz ESG x Financeiro")

    try:
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv'

        df_empresas = carregar_dados_empresas(url)

        st.write("Dados carregados da planilha:", df_empresas)

        df_empresas = calcular_scores(df_empresas)

        nova_empresa = {
            'Empresa': 'Nova Empresa',
            'Score ESG': st.session_state.score_esg,
            'Score Financeiro': st.session_state.score_financeiro
        }
        df_empresas = pd.concat([df_empresas, pd.DataFrame([nova_empresa])], ignore_index=True)

        st.plotly_chart(plotar_matriz_interativa(df_empresas), use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar os dados da planilha: {e}")
