import streamlit as st
import numpy as np

lista_indicadores = [
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


# Perguntas divididas por etapas
questions_etapa1 = [
    " Qual o segmento de atuação da empresa?",
    " Qual o setor de atuação da empresa? (Primário, Secundário ou Terciário)",
    "1. A empresa possui uma política ambiental formalizada? (1=Sim, 0=Não)",
    "2. A empresa possui relatórios de sustentabilidade auditados? (1=Sim, 0=Não)",
    "3. A empresa possui Práticas Anticorrupção? (1=Sim, 0=Não)",
    "4. A empresa possui Comitê ESG Existente? (1=Sim, 0=Não)",
    "5. A empresa possui Transparência Financeira? (1=Sim, 0=Não)"
]

questions_etapa2 = [
    "6. Qual é a emissão de carbono (CO2) da empresa em toneladas por ano?",
    "7. Qual o percentual de resíduos reciclados ou reutilizados pela empresa?",
    "8. Qual o percentual de eficiência energética (uso de energia renovável ou economia)?",
    "9. Qual o percentual de diversidade de mulheres entre os funcionários?",
    "10. Qual o percentual de diversidade de negros entre os funcionários?",
    "11. Qual o índice de satisfação dos funcionários (0 a 100)?",
    "12. Qual o valor de investimento em programas sociais (R$ M)?",
    "13. Qual o Risco Ambiental do setor? existência de riscos (0 a 10)"
]

questions_etapa3 = [
    "14. Qual a variação da ação da empresa na B3 (% YoY)?",
    "15. Qual foi o EBITDA da empresa em 2024 (R$ Bi)?",
    "16. Qual o EBITDA YoY (%)?",
    "17. Qual a margem EBITDA YoY (%)?",
    "18. Qual a posição da empresa no ranking MERCO (digite 0 se não estiver listada)?",
    "19. Quantas participações a empresa tem em índices ESG brasileiros (ISE B3, DJSI etc.)?",
    "20. Qual foi o lucro líquido de 2024 (R$ Bi)?",
    "22. Qual foi o lucro líquido  YOY (%)?",
    "23. Qual a margem de lucro líquida (%)?"
]

# Funções de pontuação

def calcular_score(valores, indicadores):
    nota = 0
    peso_total = 0
    for valor, indicador in zip(valores, indicadores):
        pontuacao = 0
        for faixa in indicador["faixas"]:
            minimo, maximo, nota_faixa = faixa
            if minimo <= valor <= maximo:
                pontuacao = nota_faixa
                break
        peso = indicador["peso"]
        nota += pontuacao * peso
        peso_total += peso
    return round(nota / peso_total, 2)

def etapa_1_basica(respostas):
    eliminacoes = sum([1 for r in respostas if r == 0])
    return eliminacoes < 3

def calcular_score_esg(valores):
    indicadores_esg = [i for i in lista_indicadores if i["categoria"] == "ESG"]
    return calcular_score(valores, indicadores_esg)

def calcular_score_financeiro(valores):
    indicadores_fin = [i for i in lista_indicadores if i["categoria"] == "Financeiro"]
    return calcular_score(valores, indicadores_fin)


# Streamlit
st.set_page_config(page_title="Avaliação ESG + Financeira", layout="centered")
st.title("📊 Avaliação ESG + Financeira")

def etapa1():
    st.title("Etapa 1 - Informações Básicas")

    # Entrada de nome da empresa
    nome_empresa = st.text_input("Nome da Empresa")

    # Campos sem peso (informativos)
    segmento = st.text_input("Qual o segmento de atuação da empresa?")
    setor = st.selectbox("Qual o setor de atuação da empresa? (Primário, Secundário ou Terciário)",
                         ["Primário", "Secundário", "Terciário"])

    # Perguntas com peso (indicadores binários ESG)
    perguntas_binarias = [
        "A empresa possui políticas de sustentabilidade?",
        "A empresa possui políticas de diversidade?",
        "A empresa realiza auditorias ambientais?",
        "A empresa publica relatórios ESG?",
        "A empresa está em conformidade com legislações ambientais?"
    ]

    respostas_binarias = []
    for i, pergunta in enumerate(perguntas_binarias):
        resposta = st.radio(pergunta, ["Sim", "Não"], key=f"pergunta_{i}")
        respostas_binarias.append(1 if resposta == "Sim" else 0)

    # Botão para avançar
    if st.button("Avançar para Etapa 2"):
        if not nome_empresa:
            st.warning("Por favor, preencha o nome da empresa antes de continuar.")
        else:
            # Armazenamento no session_state
            st.session_state["etapa1_concluida"] = True
            st.session_state["nome_empresa"] = nome_empresa
            st.session_state["segmento"] = segmento
            st.session_state["setor"] = setor
            st.session_state["respostas_binarias"] = respostas_binarias
            st.switch_page("etapa2.py")  # Substitua se o nome real for diferente

        st.header("Etapa 2 - Indicadores ESG")
        etapa2_resp = [st.number_input(q, min_value=0.0, format="%.2f") for q in questions_etapa2]

        score_esg = calcular_score_esg(etapa2_resp)
        st.metric("Score ESG", score_esg)

        if score_esg > 50:
            st.success("Empresa APROVADA para a Etapa 3")

            st.header("Etapa 3 - Indicadores Financeiros")
            etapa3_resp = [st.number_input(q, min_value=0.0, format="%.2f") for q in questions_etapa3]

            score_fin = calcular_score_financeiro(etapa3_resp)
            st.metric("Score Financeiro", score_fin)

            if score_fin > 60:
                st.success(f"✅ {nome} foi APROVADA na Avaliação Final!")
            else:
                st.error(f"❌ {nome} foi REPROVADA na Etapa Financeira.")
        else:
            st.error(f"❌ {nome} foi REPROVADA na Etapa ESG.")
    else:
        st.error(f"❌ {nome} foi ELIMINADA na Triagem Básica.")
