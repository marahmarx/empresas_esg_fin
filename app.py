# app.py
pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Funções de cálculo aqui: calcular_pontuacao, etapa_1_basica, etapa_2_esg, etapa_3_financeiro...

st.title("🔍 Triagem ESG + Financeira para Empresas")

nome_empresa = st.text_input("Nome da empresa:")

questions = [
    "Política ambiental formalizada (1=Sim, 0=Não)",
    "Relatórios de sustentabilidade auditados (1=Sim, 0=Não)",
    "Práticas anticorrupção (1=Sim, 0=Não)",
    "Comitê ESG existente (1=Sim, 0=Não)",
    "Transparência financeira (1=Sim, 0=Não)",
    "Emissão de carbono (toneladas/ano)",
    "Percentual de resíduos reciclados (%)",
    "Eficiência energética (%)",
    "Mulheres entre os funcionários (%)",
    "Negros entre os funcionários (%)",
    "Índice de satisfação dos funcionários (%)",
    "Investimento em programas sociais (R$ milhões)",
    "Risco ambiental do setor (0 a 10)",
    "Variação da ação YoY (%)",
    "EBITDA 2024 (R$ bilhões)",
    "EBITDA YoY (%)",
    "Margem EBITDA (%)",
    "Posição no ranking MERCO (0 se não está)",
    "Participações em índices ESG (ISE B3, DJSI etc.)",
    "Lucro líquido 2024 (R$ bilhões)",
    "Margem líquida (%)"
]

respostas = []
for pergunta in questions:
    resposta = st.number_input(pergunta, step=1.0, format="%.2f")
    respostas.append(resposta)

if st.button("Realizar Triagem"):
    if nome_empresa.strip() == "":
        st.error("Insira o nome da empresa.")
    else:
        if not etapa_1_basica(respostas):
            st.warning("❌ Eliminada na 1ª triagem.")
        else:
            score_esg, passou_esg = etapa_2_esg(respostas)
            if not passou_esg:
                st.warning(f"❌ Eliminada na 2ª triagem. Score ESG = {score_esg:.2f}")
            else:
                score_fin, passou_fin = etapa_3_financeiro(respostas)
                if not passou_fin:
                    st.warning(f"❌ Eliminada na 3ª triagem. Score Financeiro = {score_fin:.2f}")
                else:
                    st.success(f"✅ Aprovada! ESG = {score_esg:.2f}, Financeiro = {score_fin:.2f}")
                    # (Opcional: gerar matriz ESG x Financeiro aqui usando matplotlib ou plotly)

