import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# Configuração da página
st.set_page_config(
    page_title="Status Contagem de Insumos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# URL da Planilha (Exportação CSV)
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1Cxmeb_QKo0_XyYezfv5agDePLXFu7WYImgLMNzBiecI/export?format=csv'

# Cores das Regionais
REGIONAL_COLORS = {
    'RODRIGO': '#E91E63',
    'DANIELE': '#FB8C00',
    'SAMUEL': '#039BE5',
    'THAINA MARQUES': '#D81B60',
    'LUIZ ALEXANDRE': '#FFA000',
    'TARCIO': '#0288D1',
    'JUCILENE': '#C2185B',
    'CAIO': '#F57C00',
    'THAINA PRESTES': '#00BCD4',
    'EDUARDO': '#D32F2F',
    'ANDRIUS': '#F4511E',
    'TAISE': '#00838F'
}
DEFAULT_COLOR = '#424242'

# Injeção de CSS para replicar o design visual
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Fredoka:wght@300..700&display=swap');

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        background-color: #fefcf7;
    }
    
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

    .main-container {
        max-width: 1600px;
        margin: 0 auto;
        font-family: 'Fredoka', sans-serif;
    }

    .header-title {
        font-family: 'Luckiest Guy', cursive;
        text-align: center;
        margin-bottom: 1rem;
        color: #1a1a1a;
        line-height: 1.1;
    }
    
    .desktop-title { font-size: 62px; display: block; white-space: nowrap; }
    @media (max-width: 1024px) { .desktop-title { display: none; } }
    
    .mobile-title { font-size: 32px; display: none; }
    @media (max-width: 1024px) { .mobile-title { display: block; } }

    .stats-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .total-number {
        font-family: 'Luckiest Guy', cursive;
        font-size: 180px;
        line-height: 1;
        background: linear-gradient(to bottom, #FFD54F, #FF9100, #FF3D00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        -webkit-text-stroke: 1.5px #1e3a8a;
        filter: drop-shadow(0 12px 0 #1E3A8A);
    }
    
    .stats-text {
        font-family: 'Luckiest Guy', cursive;
        text-align: left;
        line-height: 0.85;
        text-transform: uppercase;
        color: #1a1a1a;
    }
    
    .stats-main-text { font-size: 60px; }
    .stats-sub-text { font-size: 36px; }
    
    @media (max-width: 768px) {
        .stats-container { gap: 0.5rem; }
        .total-number { font-size: 100px; filter: drop-shadow(0 8px 0 #1E3A8A); }
        .stats-main-text { font-size: 32px; }
        .stats-sub-text { font-size: 22px; }
    }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .card {
        background: white;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #f1f5f9;
        display: flex;
        flex-direction: column;
    }

    .card-header {
        padding: 0.75rem 1rem;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .card-title {
        font-family: 'Luckiest Guy', cursive;
        font-size: 24px;
        margin: 0;
    }

    .card-badge {
        background-color: rgba(30, 30, 30, 0.3);
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-family: 'Luckiest Guy', cursive;
    }

    .card-content {
        padding: 1rem;
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        font-size: 18px;
        color: #1e293b;
        line-height: 1.3;
    }

    .footer {
        text-align: right;
        font-size: 12px;
        color: #64748b;
        margin-top: 3rem;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [col.strip() for col in df.columns]
        mapping = {'Lojas': 'id', 'Check': 'check', 'Regional': 'regional'}
        # Ajuste flexível de nomes de colunas
        rename_map = {}
        for expected in mapping.keys():
            for actual in df.columns:
                if actual.lower() == expected.lower():
                    rename_map[actual] = mapping[expected]
        df = df.rename(columns=rename_map)
        return df[['id', 'check', 'regional']].dropna()
    except:
        return None

def main():
    # Atualização automática a cada 5 minutos
    st_autorefresh(interval=300 * 1000, key="data_refresh")
    
    df = load_data()
    
    if df is not None:
        pending_df = df[df['check'].str.lower() == 'pendente']
        total_pending = len(pending_df)
        
        # Agrupamento e Ordenação (mesma lógica do React)
        groups = pending_df.groupby('regional')['id'].apply(list).to_dict()
        sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

        # HTML do Dashboard
        cards_html = "".join([
            f'''
            <div class="card">
                <div class="card-header" style="background-color: {REGIONAL_COLORS.get(reg.upper(), DEFAULT_COLOR)}">
                    <h3 class="card-title">{reg.title()}</h3>
                    <div class="card-badge">{len(stores)}</div>
                </div>
                <div class="card-content">
                    {", ".join(map(str, stores))}
                </div>
            </div>
            ''' for reg, stores in sorted_groups
        ])

        st.markdown(f"""
        <div class="main-container">
            <div class="header-title">
                <span class="desktop-title">STATUS DE CONCLUSÃO CONTAGEM DE INSUMOS</span>
                <span class="mobile-title">STATUS DE CONCLUSÃO<br>CONTAGEM DE INSUMOS</span>
            </div>
            
            <div class="stats-container">
                <div class="total-number">{total_pending}</div>
                <div class="stats-text">
                    <span class="stats-main-text">LOJAS<br>PENDENTES</span><br>
                    <span class="stats-sub-text">NO TOTAL</span>
                </div>
            </div>
            
            <div class="grid-container">
                {cards_html}
            </div>
            
            <div class="footer">
                Gerado automaticamente • Ri Happy & PBKids
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
