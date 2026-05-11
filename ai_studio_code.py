import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(
    page_title="Status Contagem de Insumos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Link da Planilha
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

@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [col.strip().capitalize() for col in df.columns]
        mapping = {'Lojas': 'id', 'Check': 'check', 'Regional': 'regional'}
        final_mapping = {}
        for k, v in mapping.items():
            for ac in df.columns:
                if ac.lower() == k.lower():
                    final_mapping[ac] = v
                    break
        df = df.rename(columns=final_mapping)
        df = df[['id', 'check', 'regional']]
        df = df.dropna(subset=['id', 'check'])
        return df
    except Exception as e:
        return None

def main():
    # Botão de atualizar no topo
    col1, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
            st.rerun()

    df = load_data()
    
    if df is not None:
        pending_df = df[df['check'].str.lower() == 'pendente']
        total_pending = len(pending_df)
        groups = pending_df.groupby('regional')['id'].apply(list).to_dict()
        sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

        # Construção do HTML e CSS
        html_code = f"""
        <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Fredoka:wght@300..700&display=swap');
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #fefcf7;
                    font-family: 'Fredoka', sans-serif;
                    color: #1a1a1a;
                }}
                .main-container {{
                    max-width: 1560px;
                    margin: 0 auto;
                    padding: 10px;
                }}
                .header-title {{
                    font-family: 'Luckiest Guy', cursive;
                    text-align: center;
                    margin-bottom: 20px;
                    color: #1a1a1a;
                    line-height: 1.1;
                }}
                .desktop-title {{ font-size: 58px; display: block; }}
                .mobile-title {{ font-size: 28px; display: none; }}
                @media (max-width: 1024px) {{
                    .desktop-title {{ display: none; }}
                    .mobile-title {{ display: block; }}
                }}
                .stats-container {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 30px;
                    margin-bottom: 25px;
                }}
                .total-number {{
                    font-family: 'Luckiest Guy', cursive;
                    font-size: 160px;
                    line-height: 1;
                    background: linear-gradient(to bottom, #FFD54F, #FF9100, #FF3D00);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    filter: drop-shadow(0 10px 0 #1E3A8A);
                }}
                .stats-text {{
                    font-family: 'Luckiest Guy', cursive;
                    text-align: left;
                    line-height: 0.85;
                    text-transform: uppercase;
                }}
                .stats-main-text {{ font-size: 50px; }}
                .stats-sub-text {{ font-size: 30px; }}
                @media (max-width: 640px) {{
                    .stats-container {{ gap: 8px; }}
                    .total-number {{ font-size: 90px; filter: drop-shadow(0 6px 0 #1E3A8A); }}
                    .stats-main-text {{ font-size: 32px; }}
                    .stats-sub-text {{ font-size: 22px; }}
                }}
                .grid-container {{
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                    gap: 15px;
                    margin-bottom: 30px;
                }}
                .card {{
                    background: white;
                    border-radius: 20px;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.08);
                    border: 1px solid #f1f5f9;
                    display: flex;
                    flex-direction: column;
                }}
                .card-header {{
                    padding: 10px 15px;
                    color: white;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .card-title {{
                    font-family: 'Luckiest Guy', cursive;
                    font-size: 22px;
                    margin: 0;
                }}
                .card-badge {{
                    background-color: rgba(0, 0, 0, 0.2);
                    width: 36px;
                    height: 36px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    font-family: 'Luckiest Guy', cursive;
                    font-size: 18px;
                }}
                .card-content {{
                    padding: 12px;
                    font-weight: 700;
                    font-size: 20px;
                    color: #1e293b;
                    line-height: 1.2;
                }}
                .footer {{
                    text-align: right;
                    font-size: 11px;
                    font-style: italic;
                    color: #64748b;
                    margin-top: 30px;
                    opacity: 0.6;
                }}
            </style>
        </head>
        <body>
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
                    {" ".join([f'''
                    <div class="card">
                        <div class="card-header" style="background-color: {REGIONAL_COLORS.get(reg.upper(), DEFAULT_COLOR)}">
                            <div class="card-title">{reg.title()}</div>
                            <div class="card-badge">{len(stores)}</div>
                        </div>
                        <div class="card-content">{", ".join(map(str, stores))}</div>
                    </div>
                    ''' for reg, stores in sorted_groups])}
                </div>
                <div class="footer">Gerado automaticamente • Ri Happy & PBKids</div>
            </div>
        </body>
        </html>
        """
        # Renderiza usando o componente específico para HTML
        components.html(html_code, height=2000, scrolling=False)
    else:
        st.error("Erro ao carregar dados. Verifique o link da planilha.")

if __name__ == "__main__":
    main()
