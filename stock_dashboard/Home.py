import streamlit as st

st.set_page_config(layout="wide")
st.title(" Stock Dashboard ")
st.write("Welcome! I am developing dashboard for stockmarket review, live stock screening.")

import streamlit as st

# Custom CSS for ticker animation
st.markdown("""
    <style>
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: #0E1117; /* Streamlit dark background */
        color: #00FFAA; /* Neon green ticker text */
        padding: 8px 0;
        font-size: 20px;
        font-weight: 600;
        white-space: nowrap;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
    }

    .ticker {
        display: inline-block;
        animation: tickerMove 25s linear infinite;
    }

    @keyframes tickerMove {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>

    <div class="ticker-wrap">
      <div class="ticker">
        📈 NIFTY 50 ↑ 0.85% &nbsp;&nbsp;|&nbsp;&nbsp;
        💹 SENSEX ↑ 0.72% &nbsp;&nbsp;|&nbsp;&nbsp;
        🪙 BTC/USD ↓ 1.35% &nbsp;&nbsp;|&nbsp;&nbsp;
        💵 USD/INR 83.12 &nbsp;&nbsp;|&nbsp;&nbsp;
        📊 TM Portfolio +4.3% YTD &nbsp;&nbsp;|&nbsp;&nbsp;
        💼 Financial Dashboard by Tushar Shingade
      </div>
    </div>
""", unsafe_allow_html=True)
