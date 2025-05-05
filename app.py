import streamlit as st
import numpy as np

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

# Inicializa o estado de respostas caso não tenha sido definido
if 'respostas_binarias' not in st.session_state:
    st.session_state.respostas_binarias = [0] * 5  # Inicializa com 5 respostas binárias
if 'aprovada_etapa1' not in st.session_state:
    st.session_state.aprovada_etapa1 = False
if 'aprovada_etapa2' not in st.session_state:
    st.session_state.aprovada_etapa2 = False
if 'etapa_atual' not in st.session_state:
    st.session_state.etapa_atual = 1  # Começa na Etapa 1

# Função para navegar entre as etapas
def avancar_etapa():
    if st.session_state.etapa_atual == 1:
        st.session_state.etapa_atual = 2
    elif st.session_state.etapa_atual == 2:
        st.session_state.etapa_atual = 3

# Lista de indicadores com pesos e faixas (os mesmos da sua definição)
indicadores_esg = [
    {"indicador": "Emissão de CO2 (M ton)", "peso": 5.77, "faixas": [(0, 1000, 100), (1000.01, 5000, 70), (5000.01, np.inf, 40)]},
    {"indicador": "Gestão de Resíduos (%)", "peso": 5.77, "faixas": [(90, 100, 100), (70, 89.99, 70), (0, 69.99, 40)]},
    {"indicador": "Eficiência energética (%)", "peso": 5.77, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 40)]},
    {"indicador": "Diversidade e Inclusão Mulheres (%)", "peso": 5.77, "faixas": [(50, 100, 100), (30, 49.99, 70), (0, 29.99, 40)]},
    {"indicador": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 5.77, "faixas": [(50, 100, 100), (30, 49.99, 70), (0, 29.99, 40)]},
    {"indicador": "Índice de Satisfação dos Funcionários (%)", "peso": 1.92, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 40)]},
    {"indicador": "Investimento em Programas Sociais (R$ M)", "peso": 5.77, "faixas": [(1, np.inf, 100), (0, 0, 50)]},
    {"indicador": "Risco Ambiental", "peso": 3.85, "faixas": [(0, 0, 100), (1, 1, 50)]},
]

indicadores_financeiros = [
    {"indicador": "Variação da ação YoY (%)", "peso": 7.89, "faixas": [(-np.inf, 0, 0), (0.01, 10, 40), (10.01, 20, 70), (20.01, np.inf, 100)]},
    {"indicador": "EBITDA (R$ Bi)", "peso": 7.89, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "EBITDA YoY (%)", "peso": 5.26, "faixas": [(-np.inf, 0, 0), (0, 9.99, 40), (10, 14.99, 70), (15, np.inf, 100)]},
    {"indicador": "Margem EBITDA (%)", "peso": 2.63, "faixas": [(-np.inf, 0, 0), (0, 9.99, 40), (10, 19.99, 70), (20, np.inf, 100)]},
    {"indicador": "Posição no MERCO", "peso": 5.26, "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (101, np.inf, 0)]},
    {"indicador": "Participação em Índices ESG", "peso": 5.26, "faixas": [(0, 0, 40), (1, 1, 70), (2, np.inf, 100)]},
    {"indicador": "Lucro Líquido (R$ Bi)", "peso": 7.89, "faixas": [(-np.inf, 0, 0), (0, 9.99, 40), (10, 19.99, 70), (20, np.inf, 100)]},
    {"indicador": "Lucro Líquido YoY (%)", "peso": 5.26, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "Margem Líquida (%)", "peso": 2.63, "faixas": [(-np.inf, 0, 0), (0, 9.99, 40), (10, 19.99, 70), (20, np.inf, 100)]},
]

# Etapa 1 - Coleta de dados básicos (já existente)
if st.session_state.etapa_atual == 1:
    st.header("Etapa 1 - Indicadores ESG Básicos")
    perguntas_binarias = [
        "1. A empresa tem políticas de sustentabilidade?",
        "2. A empresa possui certificação ambiental?",
        "3. A empresa divulga suas metas de redução de emissão de CO2?",
        "4. A empresa adota práticas de reciclagem?",
        "5. A empresa investe em projetos sociais?"
    ]
    
    # Exibe as perguntas e armazena as respostas
    for i, p in enumerate(perguntas_binarias):
        st.session_state.respostas_binarias[i] = st.radio(p, options=[0, 1], index=st.session_state.respostas_binarias[i])

    # Botão para avançar
    if st.button("Avançar para Etapa 2"):
        if sum([1 for r in st.session_state.respostas_binarias if r == 0]) >= 3:
            st.error("❌ Empresa eliminada na triagem básica (Etapa 1).")
        else:
            st.success("✅ Empresa aprovada na triagem básica.")
            st.session_state.aprovada_etapa1 = True
            avancar_etapa()  # Avança para a Etapa 2

# Etapa 2 - Coleta de indicadores ESG Quantitativos
if st.session_state.etapa_atual == 2 and st.session_state.aprovada_etapa1:
    st.header("Etapa 2 - Indicadores ESG Quantitativos")
    
    respostas_etapa2 = []
    for indicador in indicadores_esg:
        st.subheader(indicador["indicador"])
        valor = st.number_input(f"Digite o valor para {indicador['indicador']}:", min_value=0.0, format="%.2f")
        respostas_etapa2.append((valor, indicador["peso"], indicador["faixas"]))

    if st.button("Avançar para Etapa 3"):
        score_esg = calcular_score_esg(respostas_etapa2)
        st.session_state.score_esg = score_esg
        st.metric("Score ESG", score_esg)

        if score_esg <= 50:
            st.error("❌ Empresa reprovada na Etapa ESG.")
        else:
            st.success("✅ Empresa aprovada na Etapa ESG.")
            st.session_state.aprovada_etapa2 = True
            avancar_etapa()  # Avança para a Et
# Etapa 3 - Coleta de Indicadores Financeiros
if st.session_state.etapa_atual == 3 and st.session_state.aprovada_etapa2:
    st.header("Etapa 3 - Indicadores Financeiros")

    respostas_etapa3 = []
    for indicador in indicadores_financeiros:
        st.subheader(indicador["indicador"])
        valor = st.number_input(f"Digite o valor para {indicador['indicador']}:", format="%.2f")
        respostas_etapa3.append((valor, indicador["peso"], indicador["faixas"]))

    if st.button("Calcular Resultado Final"):
        score_financeiro = calcular_score_financeiro(respostas_etapa3)
        st.session_state.score_financeiro = score_financeiro
        st.metric("Score Financeiro", score_financeiro)
        st.metric("Score ESG", st.session_state.score_esg)

        if score_financeiro > 50:
            st.success("✅ Empresa aprovada na triagem financeira.")
            st.balloons()
            st.write("### Resultado final: Empresa Aprovada 🎉")
        else:
            st.error("❌ Empresa reprovada na triagem financeira.")
            st.write("### Resultado final: Empresa Reprovada.")
