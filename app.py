import streamlit as st

# Função para calcular o score ESG (somente um exemplo)
def calcular_score_esg(respostas):
    # Logic for calculating ESG score (simplified example)
    return sum(respostas) / len(respostas)

# Função para calcular o score financeiro (somente um exemplo)
def calcular_score_financeiro(respostas):
    # Logic for calculating Financial score (simplified example)
    return sum(respostas) / len(respostas)

# Etapa 1 - Coleta de dados básicos
if 'respostas_binarias' not in st.session_state:
    st.session_state.respostas_binarias = [0] * 5  # Inicializa com 5 respostas binárias

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
        st.session_state.aprovada_etapa1 = True  # Marca que a empresa passou para a Etapa 2
        st.experimental_rerun()  # Recarrega a página para passar para a Etapa 2

# Etapa 2 - Coleta de indicadores ESG Quantitativos (exibido após aprovação na Etapa 1)
if 'aprovada_etapa1' in st.session_state and st.session_state.aprovada_etapa1:
    st.header("Etapa 2 - Indicadores ESG Quantitativos")
    
    # Perguntas da Etapa 2
    perguntas_etapa2 = [
        "6. Emissão de carbono (M toneladas/ano)",
        "7. Percentual de resíduos reciclados/reutilizados (%)",
        "8. Eficiência energética (%)",
        "9. Diversidade - mulheres (%)",
        "10. Diversidade - pessoas negras (%)",
        "11. Índice de satisfação dos funcionários (%)",
        "12. Investimento em programas sociais (R$ milhões)",
        "13. Risco ambiental do setor (0=Não há, 1=Há)"
    ]
    
    respostas_etapa2 = [st.number_input(p, min_value=0.0, format="%.2f") for p in perguntas_etapa2]

    if st.button("Avançar para Etapa 3"):
        score_esg = calcular_score_esg(st.session_state.respostas_binarias + respostas_etapa2)
        st.session_state.score_esg = score_esg  # Armazenando o score ESG calculado
        st.metric("Score ESG", score_esg)

        if score_esg <= 50:
            st.error("❌ Empresa reprovada na Etapa ESG.")
        else:
            st.success("✅ Empresa aprovada na Etapa ESG.")
            st.session_state.aprovada_etapa2 = True
            st.experimental_rerun()  # Recarrega para ir para a Etapa 3

# Etapa 3 - Coleta de dados financeiros (após aprovação nas etapas anteriores)
if 'aprovada_etapa2' in st.session_state and st.session_state.aprovada_etapa2:
    st.header("Etapa 3 - Indicadores Financeiros")

    # Perguntas da Etapa 3
    perguntas_etapa3 = [
        "14. Variação da ação na B3 (% YoY)",
        "15. EBITDA (R$ Bi)",
        "16. EBITDA YoY (%)",
        "17. Margem EBITDA (%)",
        "18. Posição no ranking MERCO (0 se não listada)",
        "19. Participações em índices ESG brasileiros",
        "20. Lucro líquido (R$ Bi)",
        "21. Lucro líquido YoY (%)",
        "22. Margem de lucro líquida (%)"
    ]

    respostas_etapa3 = [st.number_input(p, min_value=0.0, format="%.2f") for p in perguntas_etapa3]

    if st.button("Finalizar Avaliação"):
        score_fin = calcular_score_financeiro(respostas_etapa3)
        st.session_state.score_fin = score_fin  # Armazenando o score financeiro
        st.metric("Score Financeiro", score_fin)

        if score_fin > 60:
            st.success("🎉 Empresa aprovada na avaliação final!")
        else:
            st.error("❌ Empresa reprovada na Etapa Financeira.")
