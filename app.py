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
    {"indicador": "Emissão de CO2 (M ton)", "peso": 5.77, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador": "Gestão de Resíduos (%)", "peso": 5.77, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (0, 19.99, 10)]},
    {"indicador": "Eficiência energética (%)", "peso": 5.77, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (0, 19.99, 10)]},
    {"indicador": "Diversidade e Inclusão Mulheres (%)", "peso": 5.77, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (0, 19.99, 10)]},
    {"indicador": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 5.77, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (0, 19.99, 10)]},
    {"indicador": "Índice de Satisfação dos Funcionários (%)", "peso": 1.92, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 40)]},
    {"indicador": "Investimento em Programas Sociais (R$ M)", "peso": 5.77, "faixas": [(np.inf, 0, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]},
    {"indicador": "Risco Ambiental", "peso": 3.85, "faixas": [(0, 1, 100), (2, 3, 70), (4, 6, 50), (7, 8, 30), (9, 10, 30)]},
]

indicadores_financeiros = [
    {"indicador": "Variação da ação YoY (%)", "peso": 7.89, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "EBITDA (R$ Bi)", "peso": 7.89, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "EBITDA YoY (%)", "peso": 5.26, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem EBITDA (%)", "peso": 2.63, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Posição no MERCO", "peso": 5.26, "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (0, np.inf, 0)]},
    {"indicador": "Participação em Índices ESG", "peso": 5.26, "faixas": [(0, 0, 40), (1, 1, 80), (2, np.inf, 100)]},
    {"indicador": "Lucro Líquido (R$ Bi)", "peso": 7.89, "faixas": [(-np.inf, 0, 0), (0, 9.99, 80), (10, 19.99, 90), (20, np.inf, 100)]},
    {"indicador": "Lucro Líquido YoY (%)", "peso": 5.26, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem Líquida (%)", "peso": 2.63, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
]

# Etapa 1 - Coleta de dados básicos (ajustada para "Sim" e "Não")
if st.session_state.etapa_atual == 1:
    st.header("Etapa 1 - Indicadores ESG Básicos")
    perguntas_binarias = [
        "1. A empresa tem políticas de sustentabilidade?",
        "2. A empresa possui certificação ambiental?",
        "3. A empresa divulga suas metas de redução de emissão de CO2?",
        "4. A empresa adota práticas de reciclagem?",
        "5. A empresa investe em projetos sociais?"
    ]

    opcoes = {"Sim": 1, "Não": 0}

    for i, p in enumerate(perguntas_binarias):
        resposta = st.radio(p, options=list(opcoes.keys()), index=st.session_state.respostas_binarias[i])
        st.session_state.respostas_binarias[i] = opcoes[resposta]

    # Botão para avançar
    if st.button("Avançar para Etapa 2"):
        if sum([1 for r in st.session_state.respostas_binarias if r == 0]) >= 3:
            st.error("❌ Empresa eliminada na triagem básica (Etapa 1).")
        else:
            st.success("✅ Empresa aprovada na triagem básica.")
            st.session_state.aprovada_etapa1 = True
            avancar_etapa()
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

# --- Mostrar Matriz ESG x Financeiro com empresa atual e dados da planilha ---
if st.session_state.etapa_atual == 3 and st.session_state.aprovada_etapa2:
    st.header("📊 Comparativo: Matriz ESG x Financeiro")

    # 1. Carrega os dados das empresas já avaliadas (Google Sheets)
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv'
    df_empresas = pd.read_csv(url)

    # Garante que as colunas tenham os nomes corretos (ajuste conforme o seu Sheet)
    df_empresas.columns = df_empresas.columns.str.strip()
    col_esg = 'Score ESG'
    col_fin = 'Score Financeiro'

    # 2. Adiciona a nova empresa ao dataframe (não salva no Google Sheets, apenas localmente)
    nova_empresa = {
        'Empresa': 'Nova Empresa',
        col_esg: st.session_state.score_esg,
        col_fin: st.session_state.score_financeiro
    }
    df_empresas = pd.concat([df_empresas, pd.DataFrame([nova_empresa])], ignore_index=True)

    # 3. Plotagem da matriz ESG x Financeiro
    fig, ax = plt.subplots(figsize=(8, 6))
    for _, row in df_empresas.iterrows():
        if row['Empresa'] == 'Nova Empresa':
            ax.scatter(row[col_esg], row[col_fin], color='red', s=120, label='Nova Empresa')
            ax.annotate("Nova Empresa", (row[col_esg], row[col_fin]), textcoords="offset points", xytext=(0,10), ha='center', color='red')
        else:
            ax.scatter(row[col_esg], row[col_fin], color='blue', alpha=0.6)

    ax.set_xlabel("Score ESG")
    ax.set_ylabel("Score Financeiro")
    ax.set_title("Matriz ESG x Financeiro")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(True)
    st.pyplot(fig)
