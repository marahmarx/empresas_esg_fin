import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from gsheets_streamlit import GSheetsConnection

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

st.header("Etapa Unificada - Coleta de Dados")

# Dados da empresa
nome_empresa = st.text_input("Nome da Empresa")
segmento = st.text_input("Segmento de Atuação")
setor = st.selectbox("Setor Econômico", ["Primário", "Secundário", "Terciário"])

# Indicadores ESG Binários (5)
perguntas_binarias = [
    "A empresa tem políticas de sustentabilidade?",
    "A empresa possui certificação ambiental?",
    "A empresa divulga suas metas de redução de emissão de CO2?",
    "A empresa adota práticas de reciclagem?",
    "A empresa investe em projetos sociais?"
]

respostas_indicadores = {}
for i, pergunta in enumerate(perguntas_binarias, start=1):
    resposta = st.radio(f"Indicador_{i}: {pergunta}", options=["Sim", "Não"], key=f"bin_{i}")
    respostas_indicadores[f"Indicador_{i}"] = 1 if resposta == "Sim" else 0

# Indicadores ESG Quantitativos (8)
st.header("Indicadores ESG Quantitativos")
for i, indicador in enumerate(indicadores_esg, start=6):  # Começa do 6
    texto = indicador["indicador"]
    valor = st.number_input(
        f"Indicador_{i}: {texto}",
        min_value=0.0,
        format="%.2f",
        key=f"esg_{i}"
    )
    respostas_indicadores[f"Indicador_{i}"] = valor

# Indicadores Financeiros (11)
st.header("Indicadores Financeiros")
for i, indicador in enumerate(indicadores_financeiros, start=14):  # Começa do 14
    texto = indicador["indicador"]
    valor = st.number_input(
        f"Indicador_{i}: {texto}",
        format="%.2f",
        key=f"fin_{i}"
    )
    respostas_indicadores[f"Indicador_{i}"] = valor

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
# Criar o novo registro com as 3 primeiras colunas textuais e os dados ESG + Financeiro
nova_linha = {
    "Empresa": nome_empresa,
    "Segmento": segmento_empresa,
    "Setor": setor_empresa,
}

# Adiciona os 24 indicadores nomeados
nova_linha.update(respostas_indicadores)

# Conecta ao Google Sheets público (você já deve ter configurado esse nome de conexão no Streamlit Cloud)
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê os dados existentes na planilha
existing_df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv", ttl=0)

# Adiciona a nova linha
new_df = pd.DataFrame([new_row])
updated_df = pd.concat([existing_df, new_df], ignore_index=True)

# Escreve de volta para a planilha
conn.update(worksheet="Página1", data=updated_df)

st.success("Dados da empresa adicionados com sucesso à planilha!")

# Permitir o download do novo arquivo
st.download_button(
    label="Baixar CSV Atualizado",
    data=open(output_csv, "rb").read(),
    file_name="empresas_atualizado.csv",
    mime="text/csv"
)

# Mostrar os dados atualizados
st.write(df)

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
