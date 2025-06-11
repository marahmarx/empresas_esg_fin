import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# --- Funções de apoio ---
def aplicar_faixas(valor, faixas):
    for faixa in faixas:
        if faixa[0] <= valor <= faixa[1]:
            return faixa[2]
    return 0

def calcular_score(lista):
    total = 0
    for valor, peso, faixas in lista:
        total += aplicar_faixas(valor, faixas) * peso / 100
    return total

def calcular_scores(df, indicadores, tipo, impacto_setor):
    total_scores = []
    for _, row in df.iterrows():
        score_puro = 0
        for indicador in indicadores:
            valor = row.get(indicador["indicador"], np.nan)
            if pd.notna(valor):
                score_puro += aplicar_faixas(valor, indicador["faixas"]) * indicador["peso"] / 100

        # Aplicar redução setorial de apenas 5%
        fator_ajuste = 1 - (impacto_setor / 100) * 0.05
        score_ajustado = score_puro * fator_ajuste

        total_scores.append(score_ajustado)

    df[f"Score {tipo}"] = total_scores
    return df


def carregar_dados_empresas(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()

        for col in df.columns[3:]:
            df[col] = df[col].astype(str).str.replace('%', '', regex=False)
            df[col] = df[col].str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()


def plotar_matriz_interativa(df):
    if df.empty:
        st.error("Dados não carregados corretamente!")
        return

    if 'Empresa' not in df.columns or 'Score ESG' not in df.columns or 'Score Financeiro' not in df.columns:
        st.error("As colunas necessárias ('Empresa', 'Score ESG', 'Score Financeiro') não estão presentes.")
        return

    df["Categoria"] = df["Empresa"].apply(lambda x: "Nova Empresa" if x == "Nova Empresa" else "Empresas Existentes")

    fig = px.scatter(
        df,
        x='Score ESG',
        y='Score Financeiro',
        text='Empresa',
        color='Categoria',
        color_discrete_map={'Nova Empresa': 'red', 'Empresas Existentes': 'blue'},
        title="Matriz ESG x Financeiro",
        height=600
    )

    fig.update_traces(
        textposition='top center',
        mode='markers+text',
        marker=dict(size=12)
    )

    shapes = [
        dict(type="rect", x0=0, y0=0, x1=70, y1=70, fillcolor="rgba(255, 0, 0, 0.1)", line=dict(width=0)),
        dict(type="rect", x0=70, y0=0, x1=100, y1=70, fillcolor="rgba(255, 165, 0, 0.1)", line=dict(width=0)),
        dict(type="rect", x0=0, y0=70, x1=70, y1=100, fillcolor="rgba(173, 216, 230, 0.1)", line=dict(width=0)),
        dict(type="rect", x0=70, y0=70, x1=100, y1=100, fillcolor="rgba(144, 238, 144, 0.15)", line=dict(width=0)),
    ]
    fig.update_layout(shapes=shapes)
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.head())


# --- Dados fixos ---
impacto_por_setor = {
    "Beleza / Tecnologia / Serviços": 5,
    "Indústria Leve / Moda": 10,
    "Transporte / Logística": 15,
    "Químico / Agropecuário": 20,
    "Metalurgia": 25,
    "Petróleo e Gás": 30
}

indicadores_esg = [
    {"indicador": "Emissão de CO2 (M ton)", "peso": 20, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador": "Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 30)]},
    {"indicador": "Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(0, 0, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]}
]

indicadores_financeiros = [
    {"indicador": "Variação da ação YoY (%)", "peso": 20, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "EBITDA  (R$ Bi)", "peso": 10, "faixas": [(0, 1, 40), (1.01, 3, 70), (3.01, np.inf, 100)]},
    {"indicador": "EBITDA YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem EBITDA (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Lucro Líquido (R$ Bi)", "peso": 10, "faixas": [(0, 1, 40), (1.01, 3, 70), (3.01, np.inf, 100)]},
    {"indicador": "Lucro Líquido YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem Líquida (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]}
]

# --- Interface ---
st.title("Triagem ESG e Financeira - Avaliação da Empresa")

nome_empresa = st.text_input("Nome da empresa:")
setor_empresa = st.selectbox("Setor da empresa", list(impacto_por_setor.keys()))

st.header("Dados Básicos")
perguntas_binarias = [
    "1. A empresa tem políticas de sustentabilidade?",
    "2. A empresa possui certificação ambiental?",
    "3. A empresa divulga suas metas de redução de emissão de CO2?",
    "4. A empresa adota práticas de reciclagem?",
    "5. A empresa investe em projetos sociais?"
]
if nome_empresa:
    st.session_state["nome_empresa"] = nome_empresa
if setor_empresa:
    st.session_state["setor"] = setor_empresa

# Etapa Unificada - Coleta de Dados
respostas_binarias = []
for i, pergunta in enumerate(perguntas_binarias):
    resposta = st.radio(pergunta, options=["Sim", "Não"], key=f"pergunta_binaria_{i}")
    respostas_binarias.append(1 if resposta == "Sim" else 0)

st.subheader("Indicadores ESG")
respostas_esg = [
    (st.number_input(ind["indicador"], min_value=0.0, format="%.2f"), ind["peso"], ind["faixas"])
    for ind in indicadores_esg
]

st.subheader("Indicadores Financeiros")
respostas_financeiros = [
    (st.number_input(ind["indicador"], format="%.2f"), ind["peso"], ind["faixas"])
    for ind in indicadores_financeiros
]

# --- Análise e Gráficos ---
if st.button("Calcular Resultado"):
    score_esg = calcular_score(respostas_esg)
    score_fin = calcular_score(respostas_financeiros)

    st.metric("Score ESG", score_esg)
    st.metric("Score Financeiro", score_fin)

    respostas = respostas_binarias + [r[0] for r in respostas_esg] + [r[0] for r in respostas_financeiros]

    # --- Radar ---
    def gerar_grafico_radar(respostas, nome_empresa):
        indicadores = indicadores_esg + indicadores_financeiros
        pontuacoes = []
        categorias = []

        for i, indicador in enumerate(indicadores):
            valor = respostas[5 + i]
            score = aplicar_faixas(valor, indicador['faixas'])
            pontuacoes.append(score)
            categorias.append(indicador['indicador'])

        valores = pontuacoes + [pontuacoes[0]]
        angles = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        ax.fill(angles, valores, color='blue', alpha=0.25)
        ax.plot(angles, valores, color='blue', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categorias, fontsize=9, rotation=90)
        ax.set_title(f"Radar de Indicadores - {nome_empresa}", size=15)

        for angle, value in zip(angles, valores):
            ax.annotate(f"{value:.0f}",
                        xy=(angle, value),
                        xytext=(5, 5),
                        textcoords='offset points',
                        ha='center', va='center', fontsize=9)

        st.pyplot(fig)

    gerar_grafico_radar(respostas, nome_empresa)

    # --- Impacto ESG ---
    def gerar_grafico_impacto_esg(respostas):
        praticas_info = [
            ("Energia Renovável", 3, lambda x: float(x) >= 70),
            ("Redução CO2", 1, lambda x: float(x) < 5000),
            ("Diversidade de Mulheres", 4, lambda x: float(x) >= 30),
            ("Diversidade de pessoas negras", 5, lambda x: int(x) == 1),
        ]

        impactos = {
            "Energia Renovável": (2.5, 1.2),
            "Redução CO2": (3.0, 1.8),
            "Diversidade de Mulheres": (1.8, 0.8),
            "Diversidade de pessoas negras": (1.5, 0.5),
 

        praticas_ativas = []
        impacto_ebitda = []
        impacto_receita = []

        for nome, idx, condicao in praticas_info:
            try:
                if idx < len(respostas) and condicao(respostas[idx]):
                    praticas_ativas.append(nome)
                    impacto_ebitda.append(impactos[nome][0])
                    impacto_receita.append(impactos[nome][1])
            except Exception:
                continue

        if not praticas_ativas:
            st.warning("Nenhuma prática ESG ativa.")
            return

        fig = go.Figure(data=[
            go.Bar(name='EBITDA (%)', x=praticas_ativas, y=impacto_ebitda),
            go.Bar(name='Receita (%)', x=praticas_ativas, y=impacto_receita)
        ])
        fig.update_layout(
            title="Impacto das Práticas ESG",
            xaxis_title="Prática",
            yaxis_title="Impacto (%)",
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)

    gerar_grafico_impacto_esg(respostas)

    # --- Projeção de Faturamento ---
    def gerar_projecao_financeira(respostas):
        faturamento_base = 100_000_000
        margem_ebitda = respostas[15] / 100
        roi_inicial = respostas[16] / 100
        margem_lucro_liquida = respostas[18] / 100

        ebitda_inicial = faturamento_base * margem_ebitda
        lucro_inicial = faturamento_base * margem_lucro_liquida

        impacto_percentual = {
            'emissoes_carbono': 0.015,
            'diversidade_genero': 0.005,
            'transparencia': 0.01,
            'eficiencia': 0.02
        }

        bin_map = {
            'emissoes_carbono': respostas[2] == 1,
            'diversidade_genero': respostas[3] == 1,
            'transparencia': respostas[1] == 1,
            'eficiencia': respostas[0] == 1
        }

        ajuste_ebitda = 1 + sum([impacto_percentual[k] for k in bin_map if bin_map[k]])
        ajuste_lucro = 1 + 0.6 * (ajuste_ebitda - 1)
        ajuste_roi = 1 + 0.3 * (ajuste_ebitda - 1)

        anos = [2025, 2026, 2027, 2028, 2029]
        crescimento = 0.05

        ebitda_proj, lucro_proj, roi_proj = [], [], []

        for i in range(5):
            e = ebitda_inicial * ((1 + crescimento) ** i) * (ajuste_ebitda ** i)
            l = lucro_inicial * ((1 + crescimento) ** i) * (ajuste_lucro ** i)
            r = roi_inicial * (ajuste_roi ** i)

            ebitda_proj.append(e)
            lucro_proj.append(l)
            roi_proj.append(r * 100)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(anos, ebitda_proj, label="EBITDA (R$)")
        ax.plot(anos, lucro_proj, label="Lucro Líquido (R$)")
        ax.plot(anos, roi_proj, label="ROI (%)")
        ax.set_title("Projeção Financeira ESG")
        ax.set_xlabel("Ano")
        ax.set_ylabel("Valor")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    gerar_projecao_financeira(respostas)
    
    # --- Impacto ESG ---
    def gerar_grafico_impacto_esg(respostas):
        praticas_info = [
            ("Eficiência energética", 7, lambda x: float(x) >= 70),
            ("Redução CO2", 5, lambda x: float(x) < 5000),
            ("Diversidade de mulheres", 11, lambda x: float(x) >= 20),
            ("Diversidade de pessoas negras", 11, lambda x: float(x) >= 20),
        ]

        impactos = {
            "Eficiência energética": (2.5, 1.2),
            "Redução CO2": (3.0, 1.8),
            "Diversidade de mulheres": (1.8, 0.8),
            "Diversidade de pessoas negras": (1.5, 0.5),
        }

        praticas_ativas = []
        impacto_ebitda = []
        impacto_receita = []

        for nome, idx, condicao in praticas_info:
            try:
                if idx < len(respostas) and condicao(respostas[idx]):
                    praticas_ativas.append(nome)
                    impacto_ebitda.append(impactos[nome][0])
                    impacto_receita.append(impactos[nome][1])
            except Exception:
                continue

        if not praticas_ativas:
            st.warning("Nenhuma prática ESG ativa.")
            return

        fig = go.Figure(data=[
            go.Bar(name='EBITDA (%)', x=praticas_ativas, y=impacto_ebitda),
            go.Bar(name='Receita (%)', x=praticas_ativas, y=impacto_receita)
        ])
        fig.update_layout(
            title="Impacto das Práticas ESG",
            xaxis_title="Prática",
            yaxis_title="Impacto (%)",
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)

    gerar_grafico_impacto_esg(respostas)

    # --- Projeção de Faturamento ---
    def gerar_projecao_financeira(respostas):
        faturamento_base = 100_000_000
        margem_ebitda = respostas[18] / 100
        roi_inicial = respostas[19] / 100
        margem_lucro_liquida = respostas[20] / 100

        ebitda_inicial = faturamento_base * margem_ebitda
        lucro_inicial = faturamento_base * margem_lucro_liquida

        impacto_percentual = {
            'emissoes_carbono': 0.015,
            'diversidade_genero': 0.005,
            'transparencia': 0.01,
            'eficiencia': 0.02
        }

        bin_map = {
            'emissoes_carbono': respostas[2] == 1,
            'diversidade_genero': respostas[3] == 1,
            'transparencia': respostas[1] == 1,
            'eficiencia': respostas[0] == 1
        }

        ajuste_ebitda = 1 + sum([impacto_percentual[k] for k in bin_map if bin_map[k]])
        ajuste_lucro = 1 + 0.6 * (ajuste_ebitda - 1)
        ajuste_roi = 1 + 0.3 * (ajuste_ebitda - 1)

        anos = [2025, 2026, 2027, 2028, 2029]
        crescimento = 0.05

        ebitda_proj, lucro_proj, roi_proj = [], [], []

        for i in range(5):
            e = ebitda_inicial * ((1 + crescimento) ** i) * (ajuste_ebitda ** i)
            l = lucro_inicial * ((1 + crescimento) ** i) * (ajuste_lucro ** i)
            r = roi_inicial * (ajuste_roi ** i)

            ebitda_proj.append(e)
            lucro_proj.append(l)
            roi_proj.append(r * 100)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(anos, ebitda_proj, label="EBITDA (R$)")
        ax.plot(anos, lucro_proj, label="Lucro Líquido (R$)")
        ax.plot(anos, roi_proj, label="ROI (%)")
        ax.set_title("Projeção Financeira ESG")
        ax.set_xlabel("Ano")
        ax.set_ylabel("Valor")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    gerar_projecao_financeira(respostas)

    
#Gerar relatórios
import json
import os
import streamlit as st

st.subheader("📄 Relatório ESG Automatizado")

formato_relatorio = st.selectbox("Formato do Relatório", ["GRI", "SASB", "CSRD"])

if st.button("Gerar Relatório ESG"):
    try:
        # Junta todas as respostas numa única lista
        entradas = respostas_binarias + [r[0] for r in respostas_esg] + [r[0] for r in respostas_financeiros]
        respostas = []

        for entrada in entradas:
            try:
                resposta_float = float(entrada)
            except ValueError:
                resposta_float = 0.0  # fallback se algo der ruim
            respostas.append(resposta_float)

        empresa = {
            "nome_empresa": nome_empresa,
            "respostas": respostas,
            "respostas_textuais": []
        }

        def salvar_respostas(dados, arquivo="respostas_empresas.json"):
            if os.path.exists(arquivo):
                with open(arquivo, "r", encoding="utf-8") as f:
                    todas_respostas = json.load(f)
            else:
                todas_respostas = []
            todas_respostas.append(dados)
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump(todas_respostas, f, indent=4, ensure_ascii=False)

        salvar_respostas(empresa)

        def gerar_relatorio_esg_formatado(nome_empresa, respostas, formato="GRI"):
            def safe_get(index):
                return respostas[index] if index < len(respostas) else "N/A"

            estrutura = {
                "GRI": {
                    "GRI-101 (Políticas de Sustentabilidade)": safe_get(0),
                    "GRI-102 (Certificação Ambiental)": safe_get(1),
                    "GRI-103 (Metas de CO₂)": safe_get(2),
                    "GRI-104 (Reciclagem)": safe_get(3),
                    "GRI-105 (Projetos Sociais)": safe_get(4),
                    "GRI-305 (Emissão de CO₂)": safe_get(5),
                    "GRI-306 (Gestão de Resíduos)": safe_get(6),
                    "GRI-302 (Eficiência Energética)": safe_get(7),
                    "GRI-405 (Diversidade - Mulheres)": safe_get(8),
                    "GRI-406 (Diversidade - Pessoas Negras)": safe_get(9),
                    "GRI-407 (Satisfação dos Funcionários)": safe_get(10),
                    "GRI-413 (Investimentos Sociais)": safe_get(11),
                },
                "SASB": {
                    "SASB-101 (Uso de Energia Renovável)": safe_get(7),
                    "SASB-102 (Diversidade Estratégica)": safe_get(8),
                    "SASB-103 (Investimento Social)": safe_get(11),
                    "SASB-201 (EBITDA)": safe_get(13),
                    "SASB-202 (Lucro Líquido)": safe_get(16),
                },
                "CSRD": {
                    "CSRD-301 (Emissões Scope 1-3)": safe_get(5),
                    "CSRD-302 (Gestão de Resíduos e Energia)": safe_get(6),
                    "CSRD-303 (Diversidade e Inclusão)": f"{safe_get(8)} / {safe_get(9)}",
                    "CSRD-304 (Governança Social)": safe_get(10),
                    "CSRD-305 (Indicadores Financeiros ESG)": f"{safe_get(13)} / {safe_get(14)} / {safe_get(16)}",
                }
            }

            estrutura_escolhida = estrutura.get(formato.upper(), estrutura["GRI"])
            st.subheader(f"📘 Rascunho do Relatório - {formato.upper()}")
            st.markdown(f"**Empresa:** {nome_empresa}")
            for item, valor in estrutura_escolhida.items():
                st.markdown(f"- **{item}**: {valor}")


            return estrutura_escolhida

        estrutura_relatorio = gerar_relatorio_esg_formatado(nome_empresa, respostas, formato_relatorio)

        # PDF
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas

            def gerar_pdf_relatorio(nome_empresa, estrutura_relatorio, formato="GRI"):
                nome_arquivo = f"Relatorio_ESG_{nome_empresa.replace(' ', '_')}.pdf"
                c = canvas.Canvas(nome_arquivo, pagesize=A4)
                largura, altura = A4

                y = altura - 50
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, y, f"Relatório ESG - Formato {formato.upper()}")
                y -= 30
                c.setFont("Helvetica", 12)
                c.drawString(50, y, f"Empresa: {nome_empresa}")
                y -= 40

                for item, valor in estrutura_relatorio.items():
                    if y < 80:
                        c.showPage()
                        y = altura - 50
                    c.drawString(50, y, f"- {item}: {valor}")
                    y -= 20

                c.save()
                return nome_arquivo

            if estrutura_relatorio:
                pdf_path = gerar_pdf_relatorio(nome_empresa, estrutura_relatorio, formato_relatorio)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Baixar Relatório em PDF",
                        data=f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )

        except ModuleNotFoundError:
            st.warning("PDF não gerado: biblioteca 'reportlab' não instalada.")

    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar o relatório: {e}")
