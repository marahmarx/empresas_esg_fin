import streamlit as st

# Perguntas divididas por etapas
questions_etapa1 = [
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
def etapa_1_basica(respostas):
    eliminacoes = sum([1 for r in respostas if r == 0])
    return eliminacoes < 3

def calcular_score_esg(valores):
    pesos = [10, 10, 10, 10, 10, 10, 10, 10]
    nota = 0
    for i, valor in enumerate(valores):
        # Normalizações básicas para score
        if i == 0:  # Emissão de CO2 (quanto menor, melhor)
            nota += pesos[i] * max(0, (10000 - valor)/10000)
        elif i == 7:  # Risco ambiental (quanto menor, melhor)
            nota += pesos[i] * max(0, (10 - valor)/10)
        else:
            nota += pesos[i] * min(valor, 100) / 100
    return round(nota, 2)

def calcular_score_financeiro(valores):
    pesos = [10, 15, 10, 10, 10, 10, 15, 10]
    nota = 0
    for i, valor in enumerate(valores):
        if i == 4:  # Ranking MERCO (quanto menor melhor)
            nota += pesos[i] * max(0, (100 - valor)/100)
        else:
            nota += pesos[i] * min(valor, 100) / 100
    return round(nota, 2)

# Streamlit
st.set_page_config(page_title="Avaliação ESG + Financeira", layout="centered")
st.title("📊 Avaliação ESG + Financeira")

nome = st.text_input("Digite o nome da empresa")

if nome:
    st.header("Etapa 1 - Triagem Básica")
    etapa1_resp = [st.radio(q, [1, 0], horizontal=True) for q in questions_etapa1]

    if etapa_1_basica(etapa1_resp):
        st.success("Empresa APROVADA para a Etapa 2")

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
