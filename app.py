import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Primeira Parte
# Função para calcular o score ESG
def aplicar_faixas(valor, faixas):
    for faixa in faixas:
        if faixa[0] <= valor <= faixa[1]:
            return faixa[2]
    return 0  # Se o valor não se encaixar em nenhuma faixa

st.title("Triagem ESG e Financeira - Avaliação da Empresa")

# Perguntas iniciais
st.header("Dados da Empresa")
nome_empresa = st.text_input("Nome da empresa:")
segmento_empresa = st.selectbox("Segmento da empresa:", ["Primário", "Secundário", "Terciário"])

impacto_por_setor = {
    "Beleza / Tecnologia / Serviços": 5,
    "Indústria Leve / Moda": 10,
    "Transporte / Logística": 15,
    "Químico / Agropecuário": 20,
    "Metalurgia": 25,
    "Petróleo e Gás": 30
}

setor_empresa = st.selectbox("Setor da empresa", list(impacto_por_setor.keys()))

st.header("Dados Básicos")
perguntas_binarias = [
    "1. A empresa tem políticas de sustentabilidade?",
    "2. A empresa possui certificação ambiental?",
    "3. A empresa divulga suas metas de redução de emissão de CO2?",
    "4. A empresa adota práticas de reciclagem?",
    "5. A empresa investe em projetos sociais?"
]

# Lista de indicadores com pesos e faixas

indicadores_esg = [
    {"indicador": "6. Emissão de CO2 (M ton)", "peso": 20, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador": "7. Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "8. Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "9. Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador": "10. Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "11. Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 30)]},
    {"indicador": "12. Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(0, 0, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]}
]

indicadores_financeiros = [
    {"indicador": "13. Variação da ação YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "14. EBITDA (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "15. EBITDA YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "16. Margem EBITDA (%)", "peso": 5.5, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "17. Posição no MERCO", "peso": 11, "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (0, np.inf, 0)]},
    {"indicador": "18. Participação em Índices ESG", "peso": 11, "faixas": [(0, 0, 40), (1, 1, 80), (2, np.inf, 100)]},
    {"indicador": "19. Lucro Líquido (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 9.99, 80), (10, 19.99, 90), (20, np.inf, 100)]},
    {"indicador": "20. Lucro Líquido YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "21. Margem Líquida (%)", "peso": 5.5, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]}
]

# Etapa Unificada - Coleta de Dados
respostas_binarias = []
for i, pergunta in enumerate(perguntas_binarias):
    resposta = st.radio(pergunta, options=["Sim", "Não"], key=f"pergunta_binaria_{i}")
    respostas_binarias.append(1 if resposta == "Sim" else 0)

st.header("Indicadores ESG Quantitativos")
respostas_esg = []
for indicador in indicadores_esg:
    st.subheader(indicador["indicador"])
    valor = st.number_input(f"Digite o valor para {indicador['indicador']}:", min_value=0.0, format="%.2f", key=f"esg_{indicador['indicador']}")
    respostas_esg.append((valor, indicador["peso"], indicador["faixas"]))

st.header("Indicadores Financeiros")
respostas_financeiros = []
for indicador in indicadores_financeiros:
    st.subheader(indicador["indicador"])
    valor = st.number_input(f"Digite o valor para {indicador['indicador']}:", format="%.2f", key=f"fin_{indicador['indicador']}")
    respostas_financeiros.append((valor, indicador["peso"], indicador["faixas"]))

# Mostrar matriz ESG x Financeiro sempre que os scores estiverem disponíveis
def carregar_dados_empresas(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        

        # Converter as colunas para numérico (forçando erros a se tornarem NaN)
        for coluna in df.columns[3:]:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

        def normalizar_indicadores(df):
            # Indicadores que normalizam pelo maior valor
            indicadores_pct = ["6. Emissão de CO2 (M ton)", "12. Investimento em Programas Sociais (R$ M)",
                               "14. EBITDA (R$ Bi)", "19. Lucro Líquido (R$ Bi)"]

            for indicador in indicadores_pct:
                if indicador in df.columns:
                    max_val = df[indicador].max()
                    if pd.notna(max_val) and max_val > 0:
                        df[indicador] = df[indicador].apply(lambda x: (x / max_val) * 100 if pd.notna(x) else x)
                    else:
                        df[indicador] = 0  # Se não tiver max válido, zera tudo

            # Indicador 17 - Posição MERCO (inverter escala)
            col_17 = "17. Posição no MERCO"
            if col_17 in df.columns:
                def normaliza_merco(pos):
                    if pd.isna(pos) or pos == 0 or pos > 100 or pos < 1:
                        return 0.0
                    else:
                        return ((100 - (pos - 1)) / 99) * 100
                df[col_17] = df[col_17].apply(normaliza_merco)

            # Indicador 18 - Participação em Índices ESG
            col_18 = "18. Participação em Índices ESG"
            if col_18 in df.columns:
                def normaliza_18(valor):
                    if pd.isna(valor) or valor == 0:
                        return 0.0
                    elif valor > 100:
                        max_18 = df[col_18].max()
                        return (valor / max_18) * 100 if max_18 > 0 else 0.0
                    else:
                        return valor
                df[col_18] = df[col_18].apply(normaliza_18)

        normalizar_indicadores(df)
        return df

    except Exception as e:
        st.error(f"Erro ao carregar os dados da planilha: {e}")
        return None

#Alteração da nota de acordo com o setor

if setor_empresa in impacto_por_setor:
    impacto_setor = impacto_por_setor[setor_empresa]
else:
    impacto_setor = 0
fator_redutor = 1 - impacto_setor / 100

#Scores    
def calcular_scores(df, fator_redutor):
    esg_total = []
    financeiro_total = []

    for _, row in df.iterrows():
        score_esg1 = 0
        score_financeiro1 = 0

        for indicador in indicadores_esg:
            valor = row.get(indicador["indicador"], np.nan)
            if pd.notna(valor):
                score_esg1 += aplicar_faixas(valor, indicador["faixas"]) * indicador["peso"] / 100

        score_esg = score_esg1 * fator_redutor

        for indicador in indicadores_financeiros:
            valor = row.get(indicador["indicador"], np.nan)
            if pd.notna(valor):
                score_financeiro1 += aplicar_faixas(valor, indicador["faixas"]) * indicador["peso"] / 100

        score_financeiro = score_financeiro1 * fator_redutor

        esg_total.append(score_esg)
        financeiro_total.append(score_financeiro)

    df["Score ESG"] = esg_total
    df["Score Financeiro"] = financeiro_total
    return df

        
# Função para plotar com Plotly
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


if st.session_state.get('calculado'):
    st.header("📊 Comparativo: Matriz ESG x Financeiro")

    try:
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv'

        df_empresas = carregar_dados_empresas(url)
        # Corrigir indicadores percentuais (como "%", vírgula e escala)
        colunas_percentuais = [9, 15, 20, 21, 22]
        
        for i in colunas_percentuais:
            nome_coluna = df.columns[i]
            df[nome_coluna] = (
                df[nome_coluna]
                .astype(str)
                .str.replace('%', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
            df[nome_coluna] = pd.to_numeric(df[nome_coluna], errors='coerce')
            
            # Converter de decimal para percentual se necessário
            if df[nome_coluna].max() <= 1:
                df[nome_coluna] *= 100


        st.write("Dados carregados da planilha:", df_empresas)

        # Definir o fator redutor baseado no setor da nova empresa
        setor_empresa = st.session_state.get("setor", "")  # ou use o nome correto do campo
        if setor_empresa in impacto_por_setor:
            impacto_setor = impacto_por_setor[setor_empresa]
        else:
            impacto_setor = 0
        fator_redutor = 1 - impacto_setor / 100
        
        df_empresas = calcular_scores(df_empresas, fator_redutor)


        nova_empresa = {
            'Empresa': 'Nova Empresa',
            'Score ESG': st.session_state.score_esg,
            'Score Financeiro': st.session_state.score_financeiro
        }
        df_empresas = pd.concat([df_empresas, pd.DataFrame([nova_empresa])], ignore_index=True)

        st.plotly_chart(plotar_matriz_interativa(df_empresas), use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar os dados da planilha: {e}")

        

                    
                

        


                

            

        
                
