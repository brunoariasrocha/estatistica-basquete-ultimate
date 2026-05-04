import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DO BANCO ---
def criar_banco():
    conn = sqlite3.connect('estatisticas_basquete.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scouts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  data TEXT, jogo TEXT, jogador TEXT,
                  ll_t INT, ll_c INT, p2_t INT, p2_c INT, p3_t INT, p3_c INT,
                  reb_d INT, reb_o INT, assi INT, toco INT, erros INT, roubos INT, faltas INT)''')
    conn.commit()
    conn.close()

st.set_page_config(page_title="Scout Basquete", layout="wide")
criar_banco()

st.title("🏀 Scout Profissional de Jogo")

# 1. Cabeçalho do Jogo
col_jogo, col_data = st.columns(2)
with col_jogo:
    nome_jogo = st.text_input("Identificação do Jogo", placeholder="Ex: Ultimate x NTB")
with col_data:
    data_jogo = st.date_input("Data do Jogo", datetime.now())

# 2. Lista de Jogadores (Você pode editar essa lista aqui)
jogadores_padrao = [   
            # ARMADORES:
            "Nathan Brian", "Canhete", 
            # ALAS:
            "Giba", "Wesley", "Alex", "João Pedro", "Artur", "GH", "Fenando", "Hebert", "Fabrício", "Érik",
            # PIVÔS:
            "Kaio", "Muskito", "Brunão"]

# Criar um DataFrame vazio para o treinador preencher
if 'df_sessao' not in st.session_state:
    st.session_state.df_sessao = pd.DataFrame([
        {"Jogador": j, "LL_T": 0, "LL_C": 0, "2P_T": 0, "2P_C": 0, "3P_T": 0, "3P_C": 0, 
         "Reb_D": 0, "Reb_O": 0, "Assi": 0, "Toco": 0, "Erros": 0, "Roubos": 0, "Faltas": 0} 
        for j in jogadores_padrao
    ])

st.subheader("Preencha as Estatísticas")
# Tela de edição estilo Excel
df_editado = st.data_editor(st.session_state.df_sessao, use_container_width=True, hide_index=True)

if st.button("💾 Salvar Estatísticas do Jogo"):
    if nome_jogo:
        conn = sqlite3.connect('estatisticas_basquete.db')
        # Adiciona informações de jogo e data para cada linha
        df_final = df_editado.copy()
        df_final['jogo'] = nome_jogo
        df_final['data'] = data_jogo.strftime("%d/%m/%Y")
        
        # Salva no Banco de Dados
        df_final.to_sql('scouts', conn, if_exists='append', index=False)
        conn.close()
        st.success(f"Jogo '{nome_jogo}' salvo com sucesso no banco de dados!")
    else:
        st.error("Por favor, preencha o Nome do Jogo antes de salvar.")

st.divider()
st.caption("Dica: Você pode preencher como se fosse uma planilha de Excel e clicar no botão de salvar apenas uma vez ao final do jogo.")