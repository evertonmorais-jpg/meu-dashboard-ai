import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Configuração da página para ocupar toda a largura
st.set_page_config(page_title="Status Contagem Insumos", layout="wide")

# Injeção de CSS para replicar o design identicamente
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Fredoka:wght@400;600&display=swap" rel="stylesheet">
    <style>
    /* Estilos Globais */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Título Principal */
    .main-title {
        font-family: 'Luckiest Guy', cursive;
        font-size: 62px;
        line-height: 70px;
        text-align: center;
        color: #1a1a1a;
        margin-top: 20px;
        margin-bottom: 20px;
        letter-spacing: 0.05em;
    }

    /* Contador Gigante */
    .stats-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
        margin-bottom: 50px;
        padding: 20px 0;
    }

    .number-big {
        font-family: 'Luckiest Guy', cursive;
        font-size: 180px;
        line-height: 0.8;
        background: linear-gradient(to bottom, #FFD54F, #FF9100, #FF3D00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        /* Efeito de contorno e sombra identico ao React */
        filter: drop-shadow(0 12px 0 #1E3A8A);
        text-shadow: 
            -3px -3px 0 #1E3A8A,  
             3px -3px 0 #1E3A8A,
            -3px  3px 0 #1E3A8A,
             3px  3px 0 #1E3A8A;
    }

    .label-container {
        text-align: left;
        font-family: 'Luckiest Guy', cursive;
        color: #1a1a1a;
        line-height: 0.85;
        text-transform: uppercase;
    }

    .label-main { font-size: 60px; }
    .label-sub { font-size: 40px; }

    /* Cards das Regionais */
    .card {
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        margin-bottom: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        border: none;
    }

    .card-header {
        padding: 12px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    }

    .card-header span:first-child {
        font-family: 'Luckiest Guy', cursive;
        font-size: 20px;
        letter-spacing: 0.025em;
    }

    .card-badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 2px 12px;
        border-radius: 999px;
        font-family: 'Luckiest Guy', cursive;
        font-size: 18px;
    }

    .card-body {
        padding: 15px;
        font-family: 'Fredoka', sans-serif;
        font-size: 20px; /* Fonte aumentada conforme solicitado */
        font-weight: 600;
        color: #1e293b;
        line-height: 1.3;
    }
    
    /* Responsividade para Mobile */
    @media (max-width: 768px) {
        .main-title { font-size: 36px; line-height: 40px; }
        .number-big { font-size: 120px; }
        .label-main { font-size: 40px; }
        .label-sub { font-size: 25px; }
    }
    </style>
    """, unsafe_allow_html=True)

# Cores das Regionais identicas ao React
REGIONAL_COLORS = {
    'RODRIGO': '#E91E63', 'THAINA PRESTES': '#FF9800', 'SAMUEL': '#2196F3',
    'TARCIO': '#4CAF50', 'DANIELE': '#9C27B0', 'THAINA MARQUES': '#3F51B5',
    'EDUARDO': '#F44336', 'TAISE': '#00BCD4', 'CAIO': '#FFEB3B',
    'JUCILENE': '#795548', 'LUIZ ALEXANDRE': '#607D8B', 'ANDRIUS': '#8BC34A'
}
DEFAULT_COLOR = '#424242'

CSV_URL = 'https://docs.google.com/spreadsheets/d/1Cxmeb_QKo0_XyYezfv5agDePLXFu7WYImgLMNzBiecI/export?format=csv'

@st.cache_data(ttl=300) # Atualiza a cada 5 minutos
def load_data():
    try:
        response = requests.get(CSV_URL)
        df = pd.read_csv(StringIO(response.text))
        # Normaliza nomes de colunas
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Título Principal
    st.markdown('<div class="main-title">STATUS DE CONCLUSÃO<br/>CONTAGEM DE INSUMOS</div>', unsafe_allow_html=True)

    # Processamento dos Dados
    pending_df = df[df['Check'].str.lower() == 'pendente']
    total_pending = len(pending_df)

    # Cabeçalho de Estatísticas
    st.markdown(f"""
        <div class="stats-container">
            <div class="number-big">{total_pending}</div>
            <div class="label-container">
                <div class="label-main">LOJAS<br/>PENDENTES</div>
                <div class="label-sub">NO TOTAL</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Agrupamento por Regional
    regional_groups = pending_df.groupby('Regional')['Lojas'].apply(list).to_dict()
    sorted_regionals = sorted(regional_groups.items())

    # Grid de CARDS (4 colunas no desktop)
    cols_per_row = 4
    for i in range(0, len(sorted_regionals), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(sorted_regionals):
                name, stores = sorted_regionals[i + j]
                color = REGIONAL_COLORS.get(name, DEFAULT_COLOR)
                stores_text = ", ".join(map(str, stores))
                
                with cols[j]:
                    st.markdown(f"""
                        <div class="card">
                            <div class="card-header" style="background-color: {color};">
                                <span>{name}</span>
                                <span class="card-badge">{len(stores)}</span>
                            </div>
                            <div class="card-body">
                                {stores_text}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # Rodapé
    st.markdown("""
        <div style="text-align: right; color: #64748b; font-style: italic; font-size: 12px; margin-top: 30px;">
            Atualizando automaticamente a cada 5 minutos direto da Planilha Google
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Aguardando carregamento de dados...")
