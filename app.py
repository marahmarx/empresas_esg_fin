import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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
st.title("Triagem ESG e Financeira - Avaliação da Empresa")

# Perguntas iniciais
st.header("Dados da Empresa")
nome_empresa = st.text_input("Nome da empresa:")
segmento_empresa = st.text_input("Segmento da empresa:")
setor_empresa = st.selectbox("Setor da empresa:", ["Primário", "Secundário", "Terciário"])

# Etapa Unificada - Coleta de Dados

st.header("Dados Básicos")
perguntas_binarias = [
    "1. A empresa tem políticas de sustentabilidade?",
    "2. A empresa possui certificação ambiental?",
    "3. A empresa divulga suas metas de redução de emissão de CO2?",
    "4. A empresa adota práticas de reciclagem?",
    "5. A empresa investe em projetos sociais?"
]

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

# Função para plotar gráfico de radar
        def plotar_radar(df_resultados, nome_empresa):
            categorias = df_resultados['Indicador']
            valores = df_resultados['Score']
        
            # Normalização dos dados para escala 0-100 e prepara para o radar
            categorias = list(categorias)
            valores = list(valores)
            valores += valores[:1]  # fechar o gráfico
        
            angles = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
            angles += angles[:1]
        
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
            ax.fill(angles, valores, color='red', alpha=0.25)
            ax.plot(angles, valores, color='red', linewidth=2)
            ax.set_yticklabels([])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categorias, fontsize=9, rotation=90)
            ax.set_title(f"Radar de Desempenho por Indicador - {nome_empresa}", size=15, weight='bold')
            plt.tight_layout()
            plt.show()
        
        # Função para plotar impacto de melhoria de ESG no financeiro
        def plotar_impacto_melhoria_esg(score_esg, score_fin, nome_empresa):
            melhoria_esg = np.arange(0, 21, 5)  # até 20 pontos de melhoria
            melhoria_financeira_estim = [score_fin + (x * 0.4) for x in melhoria_esg]  # +0.4 por ponto ESG
        
            plt.figure(figsize=(10, 6))
            plt.plot(score_esg + melhoria_esg, melhoria_financeira_estim, marker='o', color='green')
            plt.axvline(x=score_esg, color='red', linestyle='--', label='ESG Atual')
            plt.axhline(y=score_fin, color='blue', linestyle='--', label='Financeiro Atual')
        
            for x, y in zip(score_esg + melhoria_esg, melhoria_financeira_estim):
                plt.text(x, y + 0.5, f"{y:.1f}", ha='center', fontsize=8)
        
            plt.title(f'Estimativa de Melhoria no Desempenho Financeiro com ESG - {nome_empresa}', fontsize=14, weight='bold')
            plt.xlabel('Score ESG ')
            plt.ylabel('Score Financeiro ')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            plt.tight_layout()
            plt.show()
        
        # Gráfico sobre o impacto das práticas ESG nos indicadores financeiros
        def plotar_impacto_praticas_esg():
            praticas_esg = [
                "Uso de Energia Renovável",
                "Diversidade de Gênero na Liderança",
                "Práticas Éticas na Cadeia de Suprimentos",
                "Satisfação dos Funcionários",
                "Redução de Emissões de Carbono"
            ]
            impacto_ebitda = [3, 3, 4, 6, 2]  # em pontos percentuais
            impacto_receita = [0, 2, 0, 5, 1]  # em pontos percentuais
        
            x = range(len(praticas_esg))
        
            plt.figure(figsize=(12, 6))
            plt.bar(x, impacto_ebitda, width=0.4, label='Impacto no EBITDA', align='center')
            plt.bar([p + 0.4 for p in x], impacto_receita, width=0.4, label='Impacto na Receita', align='center')
            plt.xticks([p + 0.2 for p in x], praticas_esg, rotation=45, ha='right')
            plt.ylabel('Impacto (%)')
            plt.title('Impacto das Práticas ESG nos Indicadores Financeiros')
            plt.legend()
            plt.tight_layout()
            plt.show()
        
        # Função para plotar evolução do EBITDA
        def plotar_projecao_ebitda():
            anos = [2025, 2026, 2027, 2028, 2029]
            ebitda_atual = [100, 102, 104, 106, 108]  # Crescimento sem melhorias ESG
            ebitda_melhoria_esg = [100, 105, 110, 115, 120]  # Crescimento com melhorias ESG
        
            plt.figure(figsize=(10, 5))
            plt.plot(anos, ebitda_atual, marker='o', label='Sem Melhoria ESG')
            plt.plot(anos, ebitda_melhoria_esg, marker='o', label='Com Melhoria ESG')
            plt.xlabel('Ano')
            plt.ylabel('EBITDA (R$ milhões)')
            plt.title('Projeção do EBITDA com e sem Melhoria em ESG')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            
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
                
        
        # Interface Streamlit
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
        
                # Mostrar matriz de ESG x Financeiro
                plotar_matriz_interativa(df_empresas)
        
                # Gráficos complementares
                plotar_radar(df_resultados, "Nova Empresa")
                plotar_impacto_melhoria_esg(st.session_state.score_esg, st.session_state.score_financeiro, "Nova Empresa")
                plotar_impacto_praticas_esg()
                plotar_projecao_ebitda()
        
            except Exception as e:
                st.error(f"Erro ao carregar os dados da planilha: {e}")

            
            # Anos analisados
            anos = np.arange(2018, 2023)
            
            # Retornos médios anuais aproximados (2018-2022)
            # ESG: Natura, WEG, Banco do Brasil (dados médios reais)
            retorno_esg = np.array([0.15, 0.20, 0.18, 0.10, 0.12])
            
            # Não ESG: Oi, Light, Braskem (dados médios reais e aproximados de empresas com instabilidade ou baixa performance ESG)
            retorno_nao_esg = np.array([-0.25, 0.05, -0.10, -0.03, 0.02])
            
            # Retorno do ISE B3 (dados aproximados)
            retorno_ise = np.array([0.12, 0.15, 0.10, 0.08, 0.11])
            
            # Dividend Yield médio anual (aproximado)
            dy_esg = 0.04  # 4%
            dy_nao_esg = 0.02  # 2%
            dy_ise = 0.035  # 3.5%
            
            # Cálculo do valor acumulado das ações com reinvestimento de dividendos
            valor_inicial = 100
            valor_esg = [valor_inicial]
            valor_nao_esg = [valor_inicial]
            valor_ise = [valor_inicial]
            
            for r_esg, r_nao_esg, r_ise in zip(retorno_esg, retorno_nao_esg, retorno_ise):
                valor_esg.append(valor_esg[-1] * (1 + r_esg + dy_esg))
                valor_nao_esg.append(valor_nao_esg[-1] * (1 + r_nao_esg + dy_nao_esg))
                valor_ise.append(valor_ise[-1] * (1 + r_ise + dy_ise))
            
            # Remover o valor inicial duplicado
            valor_esg = valor_esg[1:]
            valor_nao_esg = valor_nao_esg[1:]
            valor_ise = valor_ise[1:]
            
            # Plotagem do gráfico
            plt.figure(figsize=(12, 7))
            plt.plot(anos, valor_esg, marker='o', label='Empresas com práticas ESG (ex: Natura, WEG)', color='green')
            plt.plot(anos, valor_nao_esg, marker='s', label='Empresas sem ESG (ex: Oi, Light)', color='red')
            plt.plot(anos, valor_ise, marker='^', label='ISE B3 (Índice de Sustentabilidade Empresarial)', color='blue')
            plt.title('Evolução do Valor das Ações com Reinvestimento de Dividendos (2018-2022)', fontsize=14)
            plt.xlabel('Ano')
            plt.ylabel('Valor da Ação (R$)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        
        

