import streamlit as st
import pandas as pd

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="Dashboard Ri Happy - Insumos", layout="wide")

# URL da sua planilha (exportada como CSV)
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1Cxmeb_QKo0_XyYezfv5agDePLXFu7WYImgLMNzBiecI/export?format=csv'

# Mapeamento de cores das regionais
REGIONAL_COLORS = {
    'RODRIGO': '#E91E63',
    'THAINA PRESTES': '#FF5722',
    'THAINA MARQUES': '#9C27B0',
    'SAMUEL': '#2196F3',
    'TARCIO': '#4CAF50',
    'DANIELE': '#FFC107',
    'EDUARDO': '#3F51B5',
    'TAISE': '#009688',
    'JUCILENE': '#795548',
    'CAIO': '#607D8B',
    'LUIZ ALEXANDRE': '#E65100',
    'ANDRIUS': '#D32F2F',
}

# CSS Customizado para estilização (Fontes do Google e layout)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Fredoka:wght@400;700&display=swap');

    .main-title {
        font-family: 'Luckiest Guy', cursive;
        font-size: 50px;
        text-align: center;
        color: #1a1a1a;
        margin-bottom: 30px;
    }

    .main-stat-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
        margin-bottom: 40px;
    }

    .big-number {
        font-family: 'Luckiest Guy', cursive;
        font-size: 150px;
        line-height: 1;
        background: linear-gradient(to bottom, #FFD54F, #FF3D00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 8px 0 #1E3A8A);
    }

    .stat-text {
        font-family: 'Luckiest Guy', cursive;
        font-size: 40px;
        line-height: 0.9;
        color: #1a1a1a;
        text-transform: uppercase;
    }

    .regional-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        overflow: hidden;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }

    .card-header {
        padding: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        font-family: 'Luckiest Guy', cursive;
    }

    .card-body {
        padding: 12px;
        font-family: 'Fredoka', sans-serif;
        font-size: 18px;
        font-weight: bold;
        color: #334155;
    }

    .badge {
        background: rgba(255,255,255,0.2);
        padding: 2px 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar os dados
@st.cache_data(ttl=300) # Atualiza a cada 5 minutos
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Normalizando nomes de colunas
        df.columns = [c.capitalize() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Filtrar apenas as pendentes
    pending_df = df[df['Check'].str.lower() == 'pendente']
    total_pending = len(pending_df)

    # Título
    st.markdown('<h1 class="main-title">STATUS DE CONCLUSÃO CONTAGEM DE INSUMOS</h1>', unsafe_allow_html=True)

    # Destaque do Total
    st.markdown(f"""
        <div class="main-stat-container">
            <div class="big-number">{total_pending}</div>
            <div class="stat-text">LOJAS<br/>PENDENTES<br/><span style="font-size: 25px;">NO TOTAL</span></div>
        </div>
    """, unsafe_allow_html=True)

    # Agrupar por regional
    grouped = pending_df.groupby('Regional')['Lojas'].apply(list).reset_index()

    # Layout de Grid (4 colunas)
    cols = st.columns(4)
    for idx, row in grouped.iterrows():
        regional_name = row['Regional']
        stores = row['Lojas']
        color = REGIONAL_COLORS.get(regional_name, '#424242')
        
        with cols[idx % 4]:
            st.markdown(f"""
                <div class="regional-card">
                    <div class="card-header" style="background-color: {color};">
                        <span>{regional_name}</span>
                        <span class="badge">{len(stores)}</span>
                    </div>
                    <div class="card-body">
                        {", ".join(map(str, stores))}
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("Aguardando dados da planilha...")