import streamlit as st

st.set_page_config(page_title="TM Financial Dashboard", layout="wide")

# Hide Streamlit default padding for cleaner look
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- MOVING TICKER BAR ---
ticker_html = """
<style>
.ticker-container {
  width: 100%;
  overflow: hidden;
  background-color: #0E1117;
  color: #00FFAA;
  white-space: nowrap;
  box-shadow: 0px 2px 6px rgba(0,0,0,0.3);
  padding: 8px 0;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid #222;
}

.ticker-text {
  display: inline-block;
  padding-left: 100%;
  animation: ticker 25s linear infinite;
}

@keyframes ticker {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
</style>

<div class="ticker-container">
  <div class="ticker-text">
    📈 NIFTY 50 ↑ 0.85% &nbsp;&nbsp;|&nbsp;&nbsp;
    💹 SENSEX ↑ 0.72% &nbsp;&nbsp;|&nbsp;&nbsp;
    🪙 BTC/USD ↓ 1.35% &nbsp;&nbsp;|&nbsp;&nbsp;
    💵 USD/INR 83.12 &nbsp;&nbsp;|&nbsp;&nbsp;
    📊 TM Portfolio +4.3% YTD &nbsp;&nbsp;|&nbsp;&nbsp;
    💼 Financial Dashboard by Tushar Shingade
  </div>
</div>
"""

st.markdown(ticker_html, unsafe_allow_html=True)

# --- REST OF YOUR PAGE CONTENT BELOW ---
st.title("TM Financial Dashboard")
st.write("Welcome to your analytics hub — powered by Streamlit ✨")
