import streamlit as st
import pandas as pd
import time

# Set page config
st.set_page_config(
    page_title="Status Contagem de Insumos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Constants
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1Cxmeb_QKo0_XyYezfv5agDePLXFu7WYImgLMNzBiecI/export?format=csv'

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

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Fredoka:wght@300..700&display=swap');

    /* Reset some streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #fefcf7;
    }

    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    .main-container {
        max-width: 1600px;
        margin: 0 auto;
        font-family: 'Fredoka', sans-serif;
        color: #1a1a1a;
    }

    .header-title {
        font-family: 'Luckiest Guy', cursive;
        text-align: center;
        margin-bottom: 1rem;
        color: #1a1a1a;
        line-height: 1.1;
    }
    
    .desktop-title {
        font-size: 62px;
        display: block;
    }
    @media (max-width: 1024px) {
        .desktop-title { display: none; }
    }
    
    .mobile-title {
        font-size: 32px;
        display: none;
    }
    @media (max-width: 1024px) {
        .mobile-title { display: block; }
    }

    .stats-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 2rem;
        padding: 0.5rem;
    }
    
    @media (max-width: 640px) {
        .stats-container {
            gap: 0.5rem;
        }
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
    
    @media (max-width: 640px) {
        .total-number {
            font-size: 100px;
            filter: drop-shadow(0 8px 0 #1E3A8A);
        }
    }

    .stats-text {
        font-family: 'Luckiest Guy', cursive;
        text-align: left;
        line-height: 0.85;
        text-transform: uppercase;
    }
    
    .stats-main-text {
        font-size: 60px;
    }
    .stats-sub-text {
        font-size: 36px;
    }
    
    @media (max-width: 640px) {
        .stats-main-text { font-size: 36px; }
        .stats-sub-text { font-size: 24px; }
    }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .card {
        background: white;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
        letter-spacing: 0.025em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .card-badge {
        background-color: rgba(30, 30, 30, 0.3);
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-family: 'Luckiest Guy', cursive;
        font-size: 18px;
    }

    .card-content {
        padding: 0.75rem;
        flex: 1;
        font-family: 'Fredoka', sans-serif;
        font-weight: 700;
        font-size: 18px;
        color: #1e293b;
        line-height: 1.25;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .footer {
        text-align: right;
        font-size: 12px;
        font-style: italic;
        color: #64748b;
        margin-top: 2rem;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

# Data fetching function
@st.cache_data(ttl=300) # Cache for 5 minutes
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Handle case-insensitive columns
        df.columns = [col.strip().capitalize() for col in df.columns]
        
        # We need columns: Lojas, Check, Regional
        # Map them if they are differently named
        mapping = {
            'Lojas': 'id',
            'Check': 'check',
            'Regional': 'regional'
        }
        
        # Verify columns exist (some might be lowercase in CSV)
        available_cols = df.columns.tolist()
        final_mapping = {}
        for k, v in mapping.items():
            for ac in available_cols:
                if ac.lower() == k.lower():
                    final_mapping[ac] = v
                    break
        
        df = df.rename(columns=final_mapping)
        df = df[['id', 'check', 'regional']]
        df = df.dropna(subset=['id', 'check'])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def main():
    # Adding a refresh button in the top right (via columns)
    col1, col2 = st.columns([0.85, 0.15])
    with col2:
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
            st.rerun()

    df = load_data()
    
    if df is not None:
        # Process data
        pending_df = df[df['check'].str.lower() == 'pendente']
        total_pending = len(pending_df)
        
        # Group by regional
        groups = pending_df.groupby('regional')['id'].apply(list).to_dict()
        
        # Sort groups by count descending
        sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

        # Main Layout
        html_content = f"""
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
"""
        
        for reg, stores in sorted_groups:
            color = REGIONAL_COLORS.get(reg.upper(), DEFAULT_COLOR)
            stores_list = ", ".join(map(str, stores))
            html_content += f"""
        <div class="card">
            <div class="card-header" style="background-color: {color}">
                <h3 class="card-title">{reg.title()}</h3>
                <div class="card-badge">{len(stores)}</div>
            </div>
            <div class="card-content">
                {stores_list}
            </div>
        </div>
"""
            
        html_content += """
    <div class="footer">
        Gerado automaticamente • Ri Happy & PBKids
    </div>
</div>
"""
        st.markdown(html_content, unsafe_allow_html=True)
        
        # Auto-refresh mechanism (Streamlit will rerun the whole script)
        # Using a small trick with time.sleep and st.rerun
        if "last_refresh" not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        # Check if 5 minutes passed since last fetch (though cache handles it too)
        # But this trigger helps the UI update if user leaves tab open
        # Streamlit doesn't have a built-in "setInterval" for the browser, 
        # but we can use st_autorefresh or manual trigger for simple cases.
        # For now, we rely on user refresh or the cache TTL.
    else:
        st.warning("Nenhum dado encontrado na planilha.")

if __name__ == "__main__":
    main()
