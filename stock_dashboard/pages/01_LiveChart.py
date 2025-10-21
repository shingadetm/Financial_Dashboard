import os
import sys
from datetime import date, timedelta

import nsetools
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
# import yfinance as yf

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from utils import _get_history

st.title("Live Chart")

@st.cache_data
def nukk_def():
    pass

# Not tested
# def get_stock_info(symbol):
#     stock = yf.Ticker(symbol)
#     # price = stock.history(period = '1y',inderval = '1wk')
#     return stock.info, stock.quarterly_financials.T, stock.financials.T #, price




database_root_path = 'D:/Database/Share_Market/'
# Sample list of stocks or items
# stock_list = ["NIFTY 50", "RELIANCE", "TCS", "INFY", "HDFC", "ICICIBANK", "SBIN", "WIPRO", "HINDUNILVR"]
stock_list = ["NIFTY 50"]




col1, _,col2 = st.columns([9,12,3])

with col2:
    line_chart_flag = st.toggle("Show Line chart") # Horizontal layout for toggle + download
    crosshair_flag = st.toggle("Crosshair") # Horizontal layout for toggle + download
    
with col1:
    col1a, col1b, col1c = st.columns([1,1,1])
    with col1a:
        symbol = st.selectbox("Search and select a stock", stock_list) # Searchable dropdown


try:
    try:
        data = pd.read_csv(f'stock_dashboard/Data/{symbol}.csv')    
    except:
        try:
            data = pd.read_csv(database_root_path + f'Company/{symbol}.csv')
        except:
            try:
                data = pd.read_csv(database_root_path + f'Index/{symbol}.csv')
            except:
                pass
            # Add nsetool
    

        
    data.columns = data.columns.str.strip()
    data = data[['Date','Open','High',	'Low',	'Close']]
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by=['Date'],ascending=True)
    data['50sma'] = data['Close'].rolling(window=50).mean()
    data['200sma'] = data['Close'].rolling(window=200).mean()

except:
    data = pd.DataFrame(columns =['Open','High','Low','Close'])

with col1b:
    start_date = st.date_input(
        "Start Date",
        value=date.today() - timedelta(days=365),
        min_value=data['Date'].min(),
        max_value=date.today()-timedelta(days=1)
    )
with col1c:
    end_date = st.date_input(
        "End Date",
        value=date.today(),
        min_value=start_date,
        max_value=date.today()
    )
date_range = (start_date,end_date)


data = data.loc[(data['Date'] > pd.to_datetime(date_range[0])) & 
                (data['Date'] < pd.to_datetime(date_range[1])), :]
data.index = pd.to_datetime(data['Date'])
data.drop(columns='Date', inplace=True)







st.session_state.stock_price = data
fig = go.Figure(data=[
go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close']
    ),
go.Scatter(
        x=data.index,
        y=data['50sma'],
        mode='lines',
        line=dict(color='blue', width=1),
        name='50 SMA'
    ),
go.Scatter(
        x=data.index,
        y=data['200sma'],
        mode='lines',
        line=dict(color='red', width=1),
        name='200 SMA'
    )

])

if line_chart_flag:
    fig = go.Figure(data=[
        go.Scatter(
            x=data.index,       # or data["Date"] if you have a date column
            y=data["Close"],
            mode='lines',
            name='Close Price'
        )
    ])

fig.update_xaxes(
    autorange=True,
    rangeslider_visible = True,
    rangeselector = dict(
        buttons = list([
            dict(count = 1, label = "1m", step = "month", stepmode = "backward"),
            dict(count = 6, label = "6m", step = "month", stepmode = "backward"),
            dict(count = 1, label = "YTD", step = "year", stepmode = "todate"),
            dict(count = 1, label = "1y", step = "year", stepmode = "backward"),
            dict(step = "all")
        ])
    )
)

# Set figure size
fig.update_layout(
    dragmode='zoom',
    xaxis=dict(fixedrange=False),
    xaxis_rangeslider_visible=False,
    yaxis=dict(fixedrange=False),
    width=1400,   # Width in pixels
    height=700    # Height in pixels
)
fig.update_yaxes(
    autorange=True,
    tickformat=',',  # Adds comma separators (e.g., 25000 → 25,000)
)

if crosshair_flag:
    fig.update_layout(
        # hovermode='x unified',  # or 'closest' for full XY tracking
        xaxis=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikedash='dot',
            spikecolor='grey',
            spikethickness=1
        ),
        yaxis=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikedash='dot',
            spikecolor='grey',
            spikethickness=1
        ),
    #     hoverlabel=dict(
    #     bgcolor="white",
    #     font_size=12,
    #     font_family="Arial"
    # )
    )


# st.plotly_chart(fig)
st.plotly_chart(fig, use_container_width=False, config={
    "scrollZoom": True,       # Enables scroll-to-zoom
    "doubleClick": "reset",   # Double-click resets zoom
    "displayModeBar": True    # Shows toolbar for zoom/pan/save
})


col1,_ = st.columns([ 3, 10])
with col1:
    st.download_button("Download CSV", data.to_csv(index=False), file_name=f"{symbol}_chart_data.csv")






st.page_link("pages/02_Analysis.py", label="Go to Analysis")

