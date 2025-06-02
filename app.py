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

def calcular_scores(df, indicadores, tipo, fator_redutor):
    total_scores = []
    for _, row in df.iterrows():
        total = 0
        for indicador in indicadores:
            valor = row.get(indicador["indicador"], np.nan)
            if pd.notna(valor):
                total += aplicar_faixas(valor, indicador["faixas"]) * indicador["peso"] / 100
        total *= fator_redutor
        total_scores.append(total)
    df[f"Score {tipo}"] = total_scores
    return df

def carregar_dados_empresas(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()

        mapa_colunas = {
            "Emissão de CO ( M ton)": "6. Emissão de CO (M ton)",
            "Investimento em Programas Sociais (R$ M)": "12. Investimento em Programas Sociais (R$ M)",
            "EBITDA  (R$ Bi)": "14. EBITDA (R$ Bi)",
            "Lucro Líquido (R$ Bi)": "17. Lucro Líquido (R$ Bi)"
        }
        df.rename(columns=mapa_colunas, inplace=True)

        for col in df.columns[3:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

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
    {"indicador": "6. Emissão de CO (M ton)", "peso": 20, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador": "7. Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "8. Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "9. Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador": "10. Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "11. Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 30)]},
    {"indicador": "12. Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(0, 0, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]}
]

indicadores_financeiros = [
    {"indicador": "13. Variação da ação YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "14. EBITDA (R$ Bi)", "peso": 15, "faixas": [(0, 1, 40), (1.01, 3, 70), (3.01, np.inf, 100)]},
    {"indicador": "15. EBITDA YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "16. Margem EBITDA (%)", "peso": 5.5, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "17. Lucro Líquido (R$ Bi)", "peso": 15, "faixas": [(0, 1, 40), (1.01, 3, 70), (3.01, np.inf, 100)]},
    {"indicador": "18. Lucro Líquido YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "19. Margem Líquida (%)", "peso": 5.5, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]}
]
# --- Interface ---
st.title("Triagem ESG e Financeira - Avaliação da Empresa")

nome_empresa = st.text_input("Nome da empresa:")
setor_empresa = st.selectbox("Setor da empresa", list(impacto_por_setor.keys()))

if nome_empresa:
    st.session_state["nome_empresa"] = nome_empresa
if setor_empresa:
    st.session_state["setor"] = setor_empresa

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

    if score_esg > 70 and score_fin > 70:
        st.success("Empresa aprovada")
        st.balloons()
    else:
        st.error("Empresa reprovada")

# --- Comparativo ---
if "score_esg" in st.session_state and "score_fin" in st.session_state:
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv"
    df = carregar_dados_empresas(url)
    setor = st.session_state.get("setor", "")
    fator = 1 - impacto_por_setor.get(setor, 0)/100
    df = calcular_scores(df, indicadores_esg, "ESG", fator)
    df = calcular_scores(df, indicadores_financeiros, "Financeiro", fator)

    nova = {col: None for col in df.columns}
    nova.update({
        "Empresa": "Nova Empresa",
        "Score ESG": st.session_state["score_esg"],
        "Score Financeiro": st.session_state["score_fin"]
    })
    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)

    plotar_matriz(df)

    try:
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRNhswndyd9TY2LHQyP6BNO3y6ga47s5mztANezDmTIGsdNbBNekuvlgZlmQGZ-NAn0q0su2nKFRbAu/pub?gid=0&single=true&output=csv'

        df_empresas = carregar_dados_empresas(url)

        # Colunas para tratamento
        colunas_percentuais = [
            "Emissão de CO ( M ton)",
            "Investimento em Programas Sociais (R$ M)",
            "EBITDA  (R$ Bi)",
            "Lucro Líquido (R$ Bi)"
        ]

        for nome_coluna in colunas_percentuais:
            if nome_coluna in df_empresas.columns:
                # Converte para string para manipular
                df_empresas[nome_coluna] = df_empresas[nome_coluna].astype(str).str.replace('%', '', regex=False)
                df_empresas[nome_coluna] = df_empresas[nome_coluna].str.replace(',', '.', regex=False)
                df_empresas[nome_coluna] = pd.to_numeric(df_empresas[nome_coluna], errors='coerce')
                max_val = df_empresas[nome_coluna].max()
                if pd.notna(max_val) and max_val <= 1:
                    df_empresas[nome_coluna] *= 100

        # Recupera o setor da nova empresa do session_state
        setor_empresa = st.session_state.get("setor", "")
        impacto_setor = impacto_por_setor.get(setor_empresa, 0)
        fator_redutor = 1 - impacto_setor / 100

        # Chama a função para calcular scores (substitua pela sua)
        df_empresas = calcular_scores(df_empresas, fator_redutor)

        # Verifica se os scores estão no session_state, usa 0 como padrão
        score_esg = st.session_state.get('score_esg', 0)
        score_financeiro = st.session_state.get('score_financeiro', 0)

        # Cria a nova linha alinhada com todas as colunas
        nova_linha = {col: None for col in df_empresas.columns}
        nova_linha.update({
            'Empresa': 'Nova Empresa',
            'Score ESG': score_esg,
            'Score Financeiro': score_financeiro
        })

        df_empresas = pd.concat([df_empresas, pd.DataFrame([nova_linha])], ignore_index=True)
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

    except Exception as e:
        st.error(f"Erro ao carregar os dados da planilha: {e}")

        # Segunda parte: Análise visual completa
        mostrar_analise = st.button("Obter análise completa")

        if mostrar_analise:
            try:
                #Gráfico Radar
                respostas = respostas_esg + respostas_financeiros
                indicadores = indicadores_esg + indicadores_financeiros
                def avaliar_empresa(nome_empresa, respostas):
                    resultados = []
                    total_score = 0
                    score_esg = 0
                    score_financeiro = 0
                
                    for indicador_info, resposta in zip(indicadores, respostas):
                        # Ignorar os indicadores problemáticos (não percentuais)
                        if indicador_info["indicador"].startswith(("6.", "12.", "14.", "17.")):
                            continue
                
                        # Convertendo a resposta em número
                        try:
                            valor = float(resposta[0]) if isinstance(resposta, list) else float(resposta)
                        except (ValueError, TypeError, IndexError):
                            valor = 0.0
                
                        # Convertendo peso
                        try:
                            peso_raw = indicador_info["peso"]
                            peso = float(peso_raw[0]) if isinstance(peso_raw, list) else float(peso_raw)
                        except (ValueError, TypeError, IndexError):
                            peso = 0.0
                
                        # Calculando score numérico
                        try:
                            score_raw = calcular_pontuacao(valor, indicador_info["ranges"])
                            score = float(score_raw)  # garantir que é float
                        except Exception:
                            score = 0.0
                
                        weighted_score = score * peso / 100
                
                        # Classificando
                        if indicador_info["indicador"].startswith(("13.", "14.", "15.", "16.", "17.", "18.", "19.", "20.", "21.", "22.")):
                            score_financeiro += weighted_score
                        else:
                            score_esg += weighted_score
                
                        resultados.append({
                            "Indicador": indicador_info["indicador"],
                            "Valor": valor,
                            "Score": score,
                            "Peso (%)": peso,
                            "Score Ponderado": weighted_score
                        })
                
                        total_score += weighted_score
                
                    df_resultados = pd.DataFrame(resultados)
                    return df_resultados, total_score, score_esg, score_financeiro

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

                df_resultados, total, esg, financeiro = avaliar_empresa(nome_empresa, respostas)
                plotar_radar(df_resultados, nome_empresa)

                
                    # Gráfico de impacto ESG
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
        
                # Projeção do EBITDA
                def plotar_projecao_ebitda():
                    anos = [2025, 2026, 2027, 2028, 2029]
                    ebitda_atual = [100, 102, 104, 106, 108]
                    ebitda_melhoria_esg = [100, 105, 110, 115, 120]
        
                    plt.figure(figsize=(10, 5))
                    plt.plot(anos, ebitda_atual, marker='o', label='Sem Melhoria ESG')
                    plt.plot(anos, ebitda_melhoria_esg, marker='o', label='Com Melhoria ESG')
                    plt.xlabel('Ano')
                    plt.ylabel('EBITDA (R$ milhões)')
                    plt.title('Projeção do EBITDA com e sem Melhoria ESG')
                    plt.legend()
                    plt.grid(True)
                    plt.tight_layout()
                    st.pyplot(plt.gcf())
                    plt.close()
        
                plotar_projecao_ebitda()
        
            except Exception as e:
                st.error(f"Erro ao carregar os dados ou gerar os gráficos: {e}")

            

        
        



        


                

            

        
                
