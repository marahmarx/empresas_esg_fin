import streamlit as stMore actions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Função para calcular o score ESG
def aplicar_faixas(valor, faixas):
    for faixa in faixas:
        if faixa[0] <= valor <= faixa[1]:
            return faixa[2]
    return 0

# Lista de indicadores com pesos e faixas (os mesmos da sua definição)

indicadores_esg = [
    {"indicador": "6. Emissão de CO2 (M ton)", "peso": 20, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador": "7. Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "8. Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "9. Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador": "10. Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador": "11. Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 30)]},
    {"indicador": "12. Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(np.inf, 0, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]},
    {"indicador 6": "Emissão de CO2 (M ton)", "peso": 20, "faixas": [(0, 10, 100), (10.01, 50, 70), (50.01, np.inf, 40)]},
    {"indicador 7": "Gestão de Resíduos (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador 8": "Eficiência energética (%)", "peso": 15, "faixas": [(90, 100, 100), (60, 89.99, 70), (40, 59.99, 50), (20, 39.99, 30), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador 9": "Diversidade e Inclusão Mulheres (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10, 19.99, 10), (0, 10, 0)]},
    {"indicador 10": "Diversidade e Inclusão Pessoas Negras (%)", "peso": 15, "faixas": [(50, 100, 100), (40, 49.99, 90), (20, 39.99, 40), (10.1, 19.99, 10), (0, 10, 0)]},
    {"indicador 11": "Índice de Satisfação dos Funcionários (%)", "peso": 5, "faixas": [(80, 100, 100), (50, 79.99, 70), (0, 49.99, 30)]},
    {"indicador 12": "Investimento em Programas Sociais (R$ M)", "peso": 15, "faixas": [(np.inf, 0, 0), (1, 5, 40), (6, 20, 70), (21, np.inf, 100)]},
]

indicadores_financeiros = [
    {"indicador": "13. Variação da ação YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "14. EBITDA (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador": "15. EBITDA YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "16. Margem EBITDA (%)", "peso": 5.5 , "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "17. Posição no MERCO", "peso": 11, "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (0, np.inf, 0)]},
    {"indicador": "18. Participação em Índices ESG", "peso": 11, "faixas": [(0, 0, 40), (1, 1, 80), (2, np.inf, 100)]},
    {"indicador": "19. Lucro Líquido (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 9.99, 80), (10, 19.99, 90), (20, np.inf, 100)]},
    {"indicador": "20. Lucro Líquido YoY (%)", "peso": 11, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador": "21. Margem Líquida (%)", "peso": 5.5, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador 13": "Variação da ação YoY (%)", "peso": 15, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador 14": "EBITDA (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 29.99, 40), (30, 49.99, 70), (50, np.inf, 100)]},
    {"indicador 15": "EBITDA YoY (%)", "peso": 11, "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador 16": "Margem EBITDA (%)", "peso": 5.5 , "faixas": [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador 17": "Posição no MERCO", "peso": 11, "faixas": [(1, 30, 100), (31, 60, 70), (61, 100, 40), (0, np.inf, 0)]},
    {"indicador 18": "Participação em Índices ESG", "peso": 11, "faixas": [(0, 0, 40), (1, 1, 80), (2, np.inf, 100)]},
    {"indicador 19": "Lucro Líquido (R$ Bi)", "peso": 15, "faixas": [(-np.inf, 0, 0), (0, 9.99, 80), (10, 19.99, 90), (20, np.inf, 100)]},
    {"indicador 20": "Lucro Líquido YoY (%)", "peso": 11, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
    {"indicador 21": "Margem Líquida (%)", "peso": 5.5, "faixas":  [(-np.inf, 0, 10), (0.01, 15, 80), (15.01, 20, 90), (20.01, np.inf, 100)]},
]
st.title("Triagem ESG e Financeira - Avaliação da Empresa")

@@ -72,20 +72,23 @@
    respostas_binarias.append(1 if resposta == "Sim" else 0)

st.header("Indicadores ESG Quantitativos")

respostas_esg = []
for indicador in indicadores_esg:
    st.subheader(indicador["indicador"])
    valor = st.number_input(f"Digite o valor para {indicador['indicador']}:", min_value=0.0, format="%.2f", key=f"esg_{indicador['indicador']}")
    respostas_esg.append((valor, indicador["peso"], indicador["faixas"]))

    nome_chave = list(indicador.keys())[0]  # Ex: "indicador 6"
    nome_indicador = indicador[nome_chave]  # Ex: "Emissão de CO2 (M ton)"
    st.subheader(f"{nome_chave} - {nome_indicador}")
    valor = st.number_input(f"Digite o valor para {nome_chave} - {nome_indicador}:", min_value=0.0, format="%.2f", key=f"esg_{nome_chave}")
    respostas_esg.append(valor)

st.header("Indicadores Financeiros")
respostas_financeiros = []
for indicador in indicadores_financeiros:
    st.subheader(indicador["indicador"])
    valor = st.number_input(f"Digite o valor para {indicador['indicador']}:", format="%.2f", key=f"fin_{indicador['indicador']}")
    respostas_financeiros.append((valor, indicador["peso"], indicador["faixas"]))     
    nome_chave = list(indicador.keys())[0]  # Ex: "indicador 13"
    nome_indicador = indicador[nome_chave]  # Ex: "Variação da ação YoY (%)"
    st.subheader(f"{nome_chave} - {nome_indicador}")
    valor = st.number_input(f"Digite o valor para {nome_chave} - {nome_indicador}:", format="%.2f", key=f"fin_{nome_chave}")
    respostas_financeiros.append(valor)
  

# Mostrar matriz ESG x Financeiro sempre que os scores estiverem disponíveis

@@ -275,74 +278,84 @@
            try:
                # Gráfico Radar 

                def avaliar_empresa(nome_empresa, respostas_binarias, respostas_quantitativas):
                def avaliar_empresa(nome_empresa, respostas_binarias, respostas_esg, respostas_financeiros):
                    resultados = []
                    total_score = 0
                    total_peso = 0

                    # Processa perguntas binárias (5 itens, cada um com peso fixo, por exemplo 5)
                    peso_binario = 5  # ou qualquer valor proporcional
                    # Processa perguntas binárias (peso fixo, ex: 5)
                    peso_binario = 5
                    for pergunta, resposta in zip(perguntas_binarias, respostas_binarias):
                        score = calcular_score_binario(resposta)
                        weighted_score = score * peso_binario / 100
                        total_score += weighted_score
                        total_peso += peso_binario
                        resultados.append({
                            "Indicador": pergunta,
                            "Valor": resposta,
                            "Valor": "Sim" if resposta == 1 else "Não",
                            "Score": score,
                            "Peso (%)": peso_binario,
                            "Score Ponderado": weighted_score
                        })

                    # Processa os indicadores ESG e financeiros (quantitativos)
                    indicadores = indicadores_esg + indicadores_financeiros
                    for indicador_info, resposta in zip(indicadores, respostas_quantitativas):
                        score = calcular_score_faixas(resposta, indicador_info["faixas"])
                        peso = indicador_info["peso"]
                    # Processa indicadores ESG
                    for (valor, peso, faixas), indicador in zip(respostas_esg, indicadores_esg):
                        nome_chave = [k for k in indicador if k not in ["peso", "faixas"]][0]
                        nome_indicador = indicador[nome_chave]
                        score = calcular_score_faixas(valor, faixas)
                        weighted_score = score * peso / 100
                        total_score += weighted_score
                        total_peso += peso
                        resultados.append({
                            "Indicador": indicador_info["indicador"],
                            "Valor": resposta,
                            "Indicador": f"{nome_chave} - {nome_indicador}",
                            "Valor": valor,
                            "Score": score,
                            "Peso (%)": peso,
                            "Score Ponderado": weighted_score
                        })

                    df_resultados = pd.DataFrame(resultados)
                    # Processa indicadores financeiros
                    for (valor, peso, faixas), indicador in zip(respostas_financeiros, indicadores_financeiros):
                        nome_chave = [k for k in indicador if k not in ["peso", "faixas"]][0]
                        nome_indicador = indicador[nome_chave]
                        score = calcular_score_faixas(valor, faixas)
                        weighted_score = score * peso / 100
                        total_score += weighted_score
                        total_peso += peso
                        resultados.append({
                            "Indicador": f"{nome_chave} - {nome_indicador}",
                            "Valor": valor,
                            "Score": score,
                            "Peso (%)": peso,
                            "Score Ponderado": weighted_score
                        })

                    score_final_normalizado = total_score / (total_peso / 100)  # Normaliza para base 100
                    df_resultados = pd.DataFrame(resultados)
                    score_final_normalizado = total_score / (total_peso / 100)

                    return {
                        "nome": nome_empresa,
                        "score_total": score_final_normalizado,
                        "resultados": df_resultados
                    }

                
                def plotar_grafico_radar(df_resultados, nome_empresa):
            
                    categorias = df_resultados["Indicador"].tolist()
                    valores = df_resultados["Score"].tolist()

                    # Fecha o loop do gráfico (volta ao primeiro ponto)
                    categorias += [categorias[0]]
                    valores += [valores[0]]

                    # Ângulos para o radar
                    num_vars = len(categorias)
                    angulos = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
                    angulos += [angulos[0]]

                    # Plotagem
                    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
                    ax.plot(angulos, valores, color="blue", linewidth=2)
                    ax.fill(angulos, valores, color="skyblue", alpha=0.4)

                    # Ajuste dos rótulos
                    ax.set_xticks(angulos[:-1])
                    ax.set_xticklabels(categorias, fontsize=9)
                    ax.set_xticklabels(categorias, fontsize=9, rotation=45, ha='right')

                    ax.set_yticks([20, 40, 60, 80, 100])
                    ax.set_yticklabels(["20", "40", "60", "80", "100"])
@@ -351,69 +364,67 @@
                    plt.tight_layout()
                    plt.show()

                empresa = avaliar_empresa("Empresa Exemplo")
                empresa = avaliar_empresa("Empresa Exemplo", respostas_binarias, respostas_esg, respostas_financeiros)
                plotar_grafico_radar(empresa["resultados"], empresa["nome"])



                # Função para plotar evolução do EBITDA
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

                # Criar dataframe com resultados ESG e Financeiros
                def calcular_subscores(respostas_esg, respostas_binarias, respostas_financeiros):
                    ambiental_idx = [0, 1, 2, 3, 4]  # índices das perguntas ambientais
                    social_idx = [5, 6, 7, 8, 9, 10]  # perguntas sociais
                    governanca_idx = [11, 12, 13, 14, 15, 16]  # perguntas de governança
                    financeiro_idx = [17, 18, 19, 20, 21, 22]  # perguntas financeiras

                    grupos = {
                        "Ambiental": ambiental_idx,
                        "Social": social_idx,
                        "Governança": governanca_idx,
                        "Financeiro": financeiro_idx
                    }

                    scores = {}
                    for nome, idxs in grupos.items():
                        score = 0
                        peso_total = 0
                        for i in idxs:
                            indicador_info = indicadores[i]
                            peso_total += indicador_info["weight"]
                            valor = respostas[i]
                            score_ind = calcular_pontuacao(valor, indicador_info["ranges"])
                            weighted_score = score_ind * indicador_info["weight"] / 100
                            score += weighted_score
                        scores[nome] = round((score / (peso_total / 100)), 2)

                    return scores               


                plotar_impacto_melhoria_esg(score_esg, min(score_esg + 10, 100), "Nova Empresa")  # exemplo de melhoria
                plotar_impacto_praticas_esg()
                plotar_projecao_ebitda()

            except Exception as e:
                st.error(f"Erro ao carregar os dados ou gerar os gráficos: {e}")
