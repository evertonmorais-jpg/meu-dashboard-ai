import streamlit as st
import pandas as pd

# 1. Configurações Iniciais do Dashboard
st.set_page_config(page_title="Status Contagem Insumos", layout="wide")

# 2. Link de Exportação CSV da Planilha Google
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Cxmeb_QKo0_XyYezfv5agDePLXFu7WYImgLMNzBiecI/export?format=csv"

@st.cache_data(ttl=300) # Atualiza automaticamente a cada 5 minutos
def load_data():
    return pd.read_csv(SHEET_URL)

try:
    # Carregar Dados
    df = load_data()
    
    # Limpeza básica de nomes de colunas
    df.columns = [c.strip() for c in df.columns]
    
    # Filtrar apenas o que está "Pendente"
    pendentes_df = df[df['Check'].str.lower() == 'pendente'].copy()
    total_pendentes = len(pendentes_df)

    # 3. Título Responsivo
    st.markdown("""
        <h1 style='text-align: center; color: #1a1a1a; font-family: sans-serif; font-size: 2.5rem;'>
            STATUS DE CONCLUSÃO<br>CONTAGEM DE INSUMOS
        </h1>
    """, unsafe_allow_html=True)

    # 4. Métrica Principal
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown(f"""
            <div style='text-align: right; margin-right: 20px;'>
                <span style='font-size: 150px; font-weight: 900; color: #FF6F00; line-height: 1;'>{total_pendentes}</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style='margin-top: 25px;'>
                <h2 style='font-size: 40px; margin: 0; line-height: 0.9;'>LOJAS<br>PENDENTES</h2>
                <p style='font-size: 25px; margin: 0;'>NO TOTAL</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # 5. Cards por Regional
    regionais = sorted(pendentes_df['Regional'].unique())
    # Cria um grid de até 4 colunas
    col_grid = st.columns(4)
    
    for i, regional in enumerate(regionais):
        lojas_da_regional = pendentes_df[pendentes_df['Regional'] == regional]['Lojas'].astype(str).tolist()
        
        with col_grid[i % 4]:
            with st.container(border=True):
                st.markdown(f"### 📍 {regional}")
                st.write(f"**{len(lojas_da_regional)} pendentes:**")
                # Exibe as lojas separadas por vírgula
                st.info(", ".join(lojas_da_regional))

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.warning("Dica: Verifique se a planilha está configurada para acesso público via link.")
