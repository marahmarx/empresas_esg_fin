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
        dict(type="rect", x0=0, y0=0, x1=55, y1=60, fillcolor="rgba(255, 0, 0, 0.1)", line=dict(width=0)),
        dict(type="rect", x0=55, y0=0, x1=100, y1=60, fillcolor="rgba(255, 165, 0, 0.1)", line=dict(width=0)),
        dict(type="rect", x0=0, y0=60, x1=55, y1=100, fillcolor="rgba(173, 216, 230, 0.1)", line=dict(width=0)),
        dict(type="rect", x0=55, y0=60, x1=100, y1=100, fillcolor="rgba(144, 238, 144, 0.15)", line=dict(width=0)),
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
    {"indicador": "Emissão de CO2 (M ton)", "peso": 20, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.9, 100, 30), (100.01, np.inf, 0)]},
    {"indicador": "Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (20, 49.99, 30), (0, 19.99, 0)]},
    {"indicador": "Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(0, 0, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]}
]

indicadores_financeiros = [
    {"indicador": "Variação da ação YoY (%)", "peso": 20, "faixas": [(-np.inf, 0, 0), (0.01, 5, 20), (5.01, 15, 40), (15.01, 20, 80), (20.01, np.inf, 100)]},
    {"indicador": "EBITDA  (R$ Bi)", "peso": 10, "faixas": [(0, 0.1, 0), (0.2 , 1, 50), (1.01, 3, 70), (3.01, np.inf, 100)]},
    {"indicador": "EBITDA YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0.01, 5, 30), ( 5.01, 15, 60), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem EBITDA (%)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0.01, 5, 30), ( 5.01, 15, 60), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Lucro Líquido (R$ Bi)", "peso": 10, "faixas": [(0, 0.1, 0), (0.2 , 1, 50), (1.01, 3, 70), (3.01, np.inf, 100)]},
    {"indicador": "Lucro Líquido YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0.01, 5, 30), ( 5.01, 15, 60), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "Margem Líquida (%)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0.01, 5, 30), ( 5.01, 15, 60), (15.01, 20, 90), (20.01, np.inf, 100)]}
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

if st.button("Calcular Resultado"):
    score_esg = calcular_score(respostas_esg)
    score_fin = calcular_score(respostas_financeiros)

    st.session_state["score_esg"] = score_esg
    st.session_state["score_fin"] = score_fin
    st.metric("Score ESG", score_esg)
    st.metric("Score Financeiro", score_fin)

    if score_esg > 55 and score_fin > 60:
        st.success("Empresa aprovada")
        st.balloons()
    else:
        st.error("Empresa reprovada")

# --- Comparativo ---
if "score_esg" in st.session_state and "score_fin" in st.session_state:
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv"
    df = carregar_dados_empresas(url)
    setor = st.session_state.get("setor", "")
    impacto_setor = impacto_por_setor.get(setor, 0)  # Pega o impacto total (ex: 25)

    # Aqui aplicamos a função atualizada
    df = calcular_scores(df, indicadores_esg, "ESG", impacto_setor)
    df = calcular_scores(df, indicadores_financeiros, "Financeiro", impacto_setor)


    nova = {col: None for col in df.columns}
    nova.update({
        "Empresa": "Nova Empresa",
        "Score ESG": st.session_state["score_esg"],
        "Score Financeiro": st.session_state["score_fin"]
    })
    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)

    try:
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv'

        df_empresas = carregar_dados_empresas(url)

        colunas_percentuais = [
            "Emissão de CO ( M ton)",
            "Investimento em Programas Sociais (R$ M)",
            "EBITDA  (R$ Bi)",
            "Lucro Líquido (R$ Bi)"
        ]

        for nome_coluna in colunas_percentuais:
            if nome_coluna in df_empresas.columns:
                df_empresas[nome_coluna] = df_empresas[nome_coluna].astype(str).str.replace('%', '', regex=False)
                df_empresas[nome_coluna] = df_empresas[nome_coluna].str.replace(',', '.', regex=False)
                df_empresas[nome_coluna] = pd.to_numeric(df_empresas[nome_coluna], errors='coerce')
                max_val = df_empresas[nome_coluna].max()
                if pd.notna(max_val) and max_val <= 1:
                    df_empresas[nome_coluna] *= 100

        setor_empresa = st.session_state.get("setor", "")
        impacto_setor = impacto_por_setor.get(setor_empresa, 0)
        fator_redutor = 1 - impacto_setor / 100

        df_empresas = calcular_scores(df_empresas, indicadores_esg, "ESG", fator_redutor)
        df_empresas = calcular_scores(df_empresas, indicadores_financeiros, "Financeiro", fator_redutor)

        score_esg = st.session_state.get('score_esg', 0)
        score_financeiro = st.session_state.get('score_fin', 0)

        nova_linha = {col: None for col in df_empresas.columns}
        nova_linha.update({
            'Empresa': 'Nova Empresa',
            'Score ESG': score_esg,
            'Score Financeiro': score_financeiro
        })

        df_empresas = pd.concat([df_empresas, pd.DataFrame([nova_linha])], ignore_index=True)

        plotar_matriz_interativa(df_empresas)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Gráfico Radar
        def avaliar_empresa(nome_empresa, respostas):
            resultados = []
        
            for indicador_info, resposta in zip(indicadores, respostas):
                try:
                    valor = float(resposta[0]) if isinstance(resposta, (list, tuple)) else float(resposta)
                except (ValueError, TypeError, IndexError):
                    valor = 0.0
        
                peso = float(indicador_info.get("peso", 0))
                score_percentual = aplicar_faixas(valor, indicador_info["faixas"])
                score_ponderado = score_percentual * peso / 100
        
                resultados.append({
                    "Indicador": indicador_info["indicador"],
                    "Valor": valor,
                    "Score (%)": score_percentual,
                    "Peso (%)": peso,
                    "Score Ponderado": score_ponderado
                })
        
            df_resultados = pd.DataFrame(resultados)
            total_score = df_resultados["Score Ponderado"].sum()
            return df_resultados, total_score

        
        def plotar_radar(df_resultados, nome_empresa):
            categorias = df_resultados['Indicador']
            valores = df_resultados['Score (%)']
        
            categorias = list(categorias)
            valores = list(valores)
            valores += valores[:1]  # Fecha o círculo
        
            angles = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
            angles += angles[:1]
        
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
            ax.fill(angles, valores, color='red', alpha=0.25)
            ax.plot(angles, valores, color='red', linewidth=2)
        
            ax.set_yticklabels([])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categorias, fontsize=9, rotation=90)
            ax.set_title(f"Radar de Desempenho por Indicador - {nome_empresa}", size=15, weight='bold')
        
            # Anotar valores diretamente nos pontos
            for angle, value in zip(angles, valores):
                ax.annotate(f"{value:.0f}",
                            xy=(angle, value),
                            xytext=(5, 5),
                            textcoords='offset points',
                            ha='center', va='center', fontsize=9, color='black', weight='bold')
        
            st.pyplot(fig)
            plt.close(fig)
        
        # --- Execução final ---
        respostas = respostas_esg + respostas_financeiros
        indicadores = indicadores_esg + indicadores_financeiros
        
        df_resultados, total_score = avaliar_empresa("Nova Empresa", respostas)
        plotar_radar(df_resultados, "Nova Empresa")


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
        # Gráfico de impacto esg       
        st.markdown("### Ajuste de melhoria nos indicadores ESG")
        
        if "melhoria_eficiencia" not in st.session_state:
            st.session_state["melhoria_eficiencia"] = 10
        if "melhoria_div_mulheres" not in st.session_state:
            st.session_state["melhoria_div_mulheres"] = 10
        if "melhoria_div_negras" not in st.session_state:
            st.session_state["melhoria_div_negras"] = 10
        
        melhoria_eficiencia = st.slider(
            "Melhoria esperada em Eficiência Energética (%)",
            0, 50, st.session_state["melhoria_eficiencia"],
            key="melhoria_eficiencia"
        )
        melhoria_div_mulheres = st.slider(
            "Melhoria esperada em Diversidade (Mulheres) (%)",
            0, 50, st.session_state["melhoria_div_mulheres"],
            key="melhoria_div_mulheres"
        )
        melhoria_div_negras = st.slider(
            "Melhoria esperada em Diversidade (Pessoas Negras) (%)",
            0, 50, st.session_state["melhoria_div_negras"],
            key="melhoria_div_negras"
        )
        
        st.markdown(
            f"""
            🔋 **Eficiência Energética:** aumento de {melhoria_eficiencia}%  
            👩‍💼 **Diversidade Mulheres:** aumento de {melhoria_div_mulheres}%  
            ✊🏾 **Diversidade Negras:** aumento de {melhoria_div_negras}%
            """
        )
        
         # --- PROJEÇÃO FINANCEIRA COM CENÁRIOS ESG ---
        st.subheader("Projeção de Crescimento com Melhoria em Indicadores ESG")
    
        anos = np.arange(0, 6)
    
        # Cenários ajustados conforme setor
        cenarios_por_setor = {
            "Beleza / Tecnologia / Serviços": {"Conservador": 0.03, "Base": 0.05, "Otimista": 0.08},
            "Indústria Leve / Moda": {"Conservador": 0.025, "Base": 0.04, "Otimista": 0.065},
            "Transporte / Logística": {"Conservador": 0.02, "Base": 0.035, "Otimista": 0.06},
            "Químico / Agropecuário": {"Conservador": 0.02, "Base": 0.03, "Otimista": 0.055},
            "Metalurgia": {"Conservador": 0.015, "Base": 0.025, "Otimista": 0.04},
            "Petróleo e Gás": {"Conservador": 0.01, "Base": 0.02, "Otimista": 0.035},
        }
    
        # Cria dicionário com nome do indicador -> valor
        dict_esg = {ind["indicador"]: valor for (valor, _, _), ind in zip(respostas_esg, indicadores_esg)}
        dict_fin = {ind["indicador"]: valor for (valor, _, _), ind in zip(respostas_financeiros, indicadores_financeiros)}
    
        try:
            eficiencia_energetica = dict_esg["Eficiência energética (%)"] * (1 + melhoria_eficiencia / 100)
            diversidade_mulheres = dict_esg["Diversidade e Inclusão Mulheres (%)"] * (1 + melhoria_div_mulheres / 100)
            diversidade_negras = dict_esg["Diversidade e Inclusão Pessoas Negras (%)"] * (1 + melhoria_div_negras / 100)
    
            ebitda = dict_fin["EBITDA  (R$ Bi)"]
            lucro_liquido = dict_fin["Lucro Líquido (R$ Bi)"]
    
            crescimentos = cenarios_por_setor.get(setor_empresa, {"Conservador": 0.02, "Base": 0.03, "Otimista": 0.05})
    
            fig = go.Figure()
    
            for nome, taxa in crescimentos.items():
                fator = (1 + taxa) ** anos
                valores_ebitda = ebitda * fator
                valores_lucro = lucro_liquido * fator

                fig.add_trace(go.Scatter(
                    x=anos,
                    y=valores_ebitda,
                    mode='lines+markers+text',
                    name=f'EBITDA - {nome}',
                    text=[f"R$ {v:.2f} Bi" if i == 5 else "" for i,  v in enumerate(valores_ebitda)],
                    text=[f"R$ {v:.2f} Bi" if i == 1 else "" for i,  v in enumerate(valores_ebitda)],
                    textposition="top center"
                ))
            
                fig.add_trace(go.Scatter(
                    x=anos,
                    y=valores_lucro,
                    mode='lines+markers+text',
                    name=f'Lucro Líquido - {nome}',
                    text=[f"R$ {v:.2f} Bi" if i == 5  else "" for i, v in enumerate(valores_lucro)],
                    text=[f"R$ {v:.2f} Bi" if i == 1  else "" for i, v in enumerate(valores_lucro)],
                    textposition="bottom center"
                ))

    
            st.plotly_chart(fig, use_container_width=True)
    
        except Exception as e:
            st.error(f"Erro ao carregar os dados ou gerar os gráficos: {e}")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        st.subheader("Custo da Inação em ESG")
        
        # Penalizações por setor (% sobre EBITDA por ano)
        penalizacoes_por_setor = {
            "Beleza / Tecnologia / Serviços": 0.015,
            "Indústria Leve / Moda": 0.02,
            "Transporte / Logística": 0.025,
            "Químico / Agropecuário": 0.03,
            "Metalurgia": 0.035,
            "Petróleo e Gás": 0.04
        }
        
        # Obtemos os mesmos dados anteriores
        ebitda_base = ebitda
        anos = np.arange(0, 6)
        
        # Obter taxa de penalização e taxa de crescimento com base no setor
        penalizacao = penalizacoes_por_setor.get(setor_empresa, 0.02)
        crescimentos = cenarios_por_setor.get(setor_empresa, {"Base": 0.03})
        
        # Cenário 1: Sem ESG - perda acumulada no EBITDA
        ebitda_inação = [ebitda_base * ((1 - penalizacao) ** ano) for ano in anos]
        
        # Cenário 2: Com ESG - crescimento projetado com melhoria
        taxa_crescimento = crescimentos["Base"]
        ebitda_com_melhoria = [ebitda_base * ((1 + taxa_crescimento) ** ano) for ano in anos]
        
        # Criação do gráfico
        fig_penalizacao = go.Figure()
        
        fig_penalizacao.add_trace(go.Scatter(
            x=anos,
            y=ebitda_com_melhoria,
            mode='lines+markers',
            name='Com Melhoria ESG',
            line=dict(color='green')
        ))
        
        fig_penalizacao.add_trace(go.Scatter(
            x=anos,
            y=ebitda_inação,
            mode='lines+markers',
            name='Sem Ação ESG',
            line=dict(color='red', dash='dash')
        ))
        
        # Área entre os dois cenários (valor perdido)
        fig_penalizacao.add_trace(go.Scatter(
            x=np.concatenate([anos, anos[::-1]]),
            y=np.concatenate([ebitda_com_melhoria, ebitda_inação[::-1]]),
            fill='toself',
            fillcolor='rgba(255,0,0,0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ))
        
        fig_penalizacao.update_layout(
            title="Projeção do Custo da Inação em ESG (Impacto no EBITDA)",
            xaxis_title="Ano",
            yaxis_title="EBITDA (R$ Bi)",
            legend_title="Cenário",
            template="plotly_white",
            height=500
        )
        
        st.plotly_chart(fig_penalizacao, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar os dados ou gerar os gráficos: {e}")
  
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
