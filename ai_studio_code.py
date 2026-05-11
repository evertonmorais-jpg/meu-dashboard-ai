import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

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
    # Header with Refresh button
    col1, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
            st.rerun()

    df = load_data()
    
    if df is not None:
        total_stores = len(df)
        pending_df = df[df['check'].str.lower() == 'pendente']
        ok_stores = total_stores - len(pending_df)
        completion_percentage = round((ok_stores / total_stores * 100), 1) if total_stores > 0 else 0
        
        total_pending = len(pending_df)
        groups = pending_df.groupby('regional')['id'].apply(list).to_dict()
        sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

        # Style + HTML Build
        html_code = f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Fredoka:wght@300..700&display=swap');
            body {{
                margin: 0;
                background-color: #fefcf7;
                font-family: 'Fredoka', sans-serif;
                color: #1a1a1a;
            }}
            .main-container {{
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header-title {{
                font-family: 'Luckiest Guy', cursive;
                text-align: center;
                margin-bottom: 20px;
                color: #1a1a1a;
                line-height: 1.1;
            }}
            .desktop-title {{ font-size: 62px; display: block; }}
            .mobile-title {{ font-size: 32px; display: none; }}
            @media (max-width: 1024px) {{
                .desktop-title {{ display: none; }}
                .mobile-title {{ display: block; }}
            }}
            .stats-container {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 40px;
                margin-bottom: 20px;
            }}
            .total-number {{
                font-family: 'Luckiest Guy', cursive;
                font-size: 180px;
                line-height: 1;
                background: linear-gradient(to bottom, #FFD54F, #FF9100, #FF3D00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                filter: drop-shadow(0 12px 0 #1E3A8A);
            }}
            .stats-text {{
                font-family: 'Luckiest Guy', cursive;
                text-align: left;
                line-height: 0.85;
                text-transform: uppercase;
            }}
            .stats-main-text {{ font-size: 60px; }}
            .stats-sub-text {{ font-size: 36px; }}

            /* Progress Bar Styles */
            .progress-section {{
                width: 100%;
                max-width: 1000px;
                margin: 0 auto 40px auto;
                text-align: center;
            }}
            .progress-label {{
                font-family: 'Luckiest Guy', cursive;
                font-size: 24px;
                margin-bottom: 10px;
                color: #059669;
                display: flex;
                justify-content: space-between;
                align-items: baseline;
            }}
            .progress-container-bg {{
                width: 100%;
                height: 32px;
                background-color: #e2e8f0;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                border: 4px solid white;
            }}
            .progress-bar-fill {{
                height: 100%;
                width: {completion_percentage}%;
                background: linear-gradient(90deg, #10b981 0%, #34d399 50%, #6ee7b7 100%);
                border-radius: 12px;
                box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
                transition: width 1s ease-in-out;
            }}

            @media (max-width: 640px) {{
                .stats-container {{ gap: 10px; }}
                .total-number {{ font-size: 100px; filter: drop-shadow(0 8px 0 #1E3A8A); }}
                .stats-main-text {{ font-size: 36px; }}
                .stats-sub-text {{ font-size: 24px; }}
                .progress-label {{ font-size: 18px; }}
                .progress-container-bg {{ height: 24px; }}
            }}
            .grid-container {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .card {{
                background: white;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border: 1px solid #f1f5f9;
                display: flex;
                flex-direction: column;
            }}
            .card-header {{
                padding: 12px 20px;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .card-title {{
                font-family: 'Luckiest Guy', cursive;
                font-size: 24px;
                margin: 0;
            }}
            .card-badge {{
                background-color: rgba(30, 30, 30, 0.3);
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                font-family: 'Luckiest Guy', cursive;
                font-size: 20px;
            }}
            .card-content {{
                padding: 15px;
                font-weight: 700;
                font-size: 20px;
                color: #1e293b;
                line-height: 1.3;
            }}
            .footer {{
                text-align: right;
                font-size: 12px;
                font-style: italic;
                color: #64748b;
                margin-top: 40px;
                opacity: 0.7;
            }}
        </style>
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

            <div class="progress-section">
                <div class="progress-label">
                    <span>CONTAGEM CONCLUÍDA</span>
                    <span>{completion_percentage}%</span>
                </div>
                <div class="progress-container-bg">
                    <div class="progress-bar-fill"></div>
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
        """
        # Render the HTML component
        components.html(html_code, height=1200, scrolling=True)
    else:
        st.error("Não foi possível carregar os dados. Verifique a URL da planilha.")

if __name__ == "__main__":
    main()
