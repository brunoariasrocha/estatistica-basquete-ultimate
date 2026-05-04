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
                  Data TEXT, Jogo TEXT, Jogador TEXT,
                  LL_T INT, LL_C INT, P2_T INT, P2_C INT, P3_T INT, P3_C INT,
                  Reb_D INT, Reb_O INT, Assi INT, Toco INT, Erros INT, Roubos INT, Faltas INT)''')
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
    data_jogo = st.date_input("Data do Jogo", datetime.now(), format="DD/MM/YYYY")

# 2. LISTA MESTRA DE ATLETAS (Adicione os 50+ nomes aqui)
elenco_completo = sorted([
    "Nathan Brian", "Canhete", "Giba", "Wesley", "Alex", "João Pedro", 
    "Artur", "GH", "Fernando", "Hebert", "Fabrício", "Érik", "Kaio", 
    "Muskito", "Brunão" # ... complete a lista
])

st.divider()

# 3. SELEÇÃO DE QUEM VAI PRO JOGO
st.subheader("1. Selecione os Atletas que participaram")
jogadores_selecionados = st.multiselect(
    "Clique ou digite os nomes dos relacionados:", 
    options=elenco_completo,
    help="Apenas os nomes selecionados aqui aparecerão na tabela de estatísticas."
)

if jogadores_selecionados:
    st.subheader("2. Preencha as Estatísticas")
    
    # Criamos a tabela dinamicamente apenas para os selecionados
    df_para_preencher = pd.DataFrame([
        {"Jogador": j, "LL_T": 0, "LL_C": 0, "P2_T": 0, "P2_C": 0, "P3_T": 0, "P3_C": 0, 
         "Reb_D": 0, "Reb_O": 0, "Assi": 0, "Toco": 0, "Erros": 0, "Roubos": 0, "Faltas": 0} 
        for j in jogadores_selecionados
    ])

    # Tela de edição
    df_editado = st.data_editor(df_para_preencher, use_container_width=True, hide_index=True)

    if st.button("💾 Salvar Estatísticas do Jogo"):
        if nome_jogo:
            try:
                conn = sqlite3.connect('estatisticas_basquete.db')
                df_final = df_editado.copy()
                df_final['Jogo'] = nome_jogo
                df_final['Data'] = data_jogo.strftime("%d/%m/%Y")
                
                # Salva apenas quem foi selecionado
                df_final.to_sql('scouts', conn, if_exists='append', index=False)
                conn.close()
                
                st.success(f"Dados salvos! {len(jogadores_selecionados)} jogadores registrados para '{nome_jogo}'.")
                st.balloons()
            except Exception as e:
                st.error(f"Erro técnico ao salvar: {e}")
        else:
            st.error("Por favor, preencha o Nome do Jogo.")
else:
    st.info("Selecione pelo menos um jogador acima para abrir a tabela de preenchimento.")

st.divider()
st.caption("Dica: O banco de dados agora conterá apenas os registros de quem realmente entrou em quadra.")