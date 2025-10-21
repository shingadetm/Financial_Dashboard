import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.markdown("<h1 style='text-align: center;'> Stock Analysis</h1>", unsafe_allow_html=True)

def html_table(data,index = True):
    styled_table = data.style.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]}]
    ) # .hide(axis='index')  # hides the index column 
    if index==False:
        styled_table = styled_table.hide(axis='index')  
    return styled_table

def cal_max_drawdown(series):
    cumulative = (1 + series).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()



if "stock_price" in st.session_state:
    col1, col2 = st.columns([1,1])
    # Load price data (e.g., from CSV or API)
    
    price = st.session_state.stock_price

    price = price.sort_values(by=['Date'],ascending=True)
    price['Returns'] = price['Close'].pct_change()*100
    start_date = (price.index.min()).strftime("%d %b %Y")
    end_date = (price.index.max()).strftime("%d %b %Y")
    with col1:
        # st.write(f"From : { start_date }    To : { end_date }")
        msg = f"From : { start_date }    To : { end_date }"
        st.markdown(f"""<h4 style='text-align: left;'>{msg}</h4>    """, unsafe_allow_html=True)
        data_overview = html_table(price.describe().round(3).astype(str))
        st.write(data_overview  .to_html(escape=False), unsafe_allow_html=True)

    # Daily returns
    returns = price['Close'].pct_change()

    # Cumulative returns
    cumulative_returns = (1 + returns).cumprod() - 1

    # Annualized return
    annualized_return = (1 + cumulative_returns.iloc[-1]) ** (252 / len(returns)) - 1

    # Volatility
    volatility = returns.std() * np.sqrt(252)

    # Sharpe Ratio
    sharpe_ratio = annualized_return / volatility

    # Max Drawdown
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = cumulative / rolling_max - 1
    max_drawdown = drawdown.min()          
    end_date = drawdown.idxmin()  # Find end date of max drawdown    
    start_date = drawdown.loc[:end_date].idxmax() # Find start date: last peak before the drawdown
    # Identify all losing periods (drawdown < 0)
    losing_periods = drawdown[drawdown < 0]
    # Group consecutive losing dates
    groups = (losing_periods.index.to_series().diff().dt.days != 1).cumsum()
    grouped = losing_periods.groupby(groups)

    performance_metrics = pd.DataFrame({
                            'Ann. Return' : str(round(annualized_return*100,2)) + '%',
                            'Volatility': str(round(volatility*100,2)) + '%',
                            'Sharpe Ratio' : str(round(sharpe_ratio,2)),
                            'Max Drawdown' : [str(round(max_drawdown*100,2)) + '%']}
                            )

    # Convert to HTML with centered text
    performance_metrics = html_table(performance_metrics,index = False)

    # Display in Streamlit
    st.markdown("### Performance Metrics")
    st.write(performance_metrics.to_html(escape=False), unsafe_allow_html=True)



     
    
    # Plot cumulative returns
    # cumulative_returns.plot(title="Cumulative Returns")
    # plt.show()
    
    fig = go.Figure(data=[
            go.Scatter(
            x=drawdown.index,       # or data["Date"] if you have a date column
            y=drawdown*100,
            mode='lines',
            name='Close Price',
            fill='tozeroy'
        )
    ])

    # Cumulative return line
    # fig.add_trace(go.Scatter(
    #     x=cumulative_returns.index,
    #     y=cumulative_returns*100,
    #     mode='lines',
    #     line=dict(color='royalblue'),
    #     name='Cumulative Return (%)'
    # ))

    # Optionally highlight the drawdown period
    fig.add_vrect(
        x0=start_date,
        x1=end_date,
        fillcolor="red",
        opacity=0.2,
        layer="below",
        line_width=0
    )

    # Set figure size
    fig.update_layout(
        dragmode='zoom',
        xaxis_title="Date",
        xaxis=dict(fixedrange=False),
        # yaxis=dict(fixedrange=False),
        yaxis_title="Drawdown (%)",
        yaxis=dict(ticksuffix="%", showgrid=True),
        width=800,   # Width in pixels
        height=400    # Height in pixels
    )
    with col2:
        st.plotly_chart(fig, use_container_width=False, config={
            "scrollZoom": False,       # Enables scroll-to-zoom
            "doubleClick": "reset",   # Double-click resets zoom
            "displayModeBar": False    # Shows toolbar for zoom/pan/save
        })    
        st.markdown("""<h4 style='text-align: center;'>Max Drawdown</h4>    """, unsafe_allow_html=True)


    ## Yearly Stats
    # Daily returns
    df = st.session_state.stock_price
    yearly_min = df['Close'].resample('Y').min()
    yearly_max = df['Close'].resample('Y').max()

    df['daily_return'] = df['Close'].pct_change()

    # Group by year
    annual_return = df['daily_return'].resample('Y').apply(lambda x: (1 + x).prod() - 1)
    annual_volatility = df['daily_return'].resample('Y').std() * np.sqrt(252)
    risk_free_rate = 0.05  # Adjust as needed
    annual_sharpe = (annual_return - risk_free_rate) / annual_volatility 
    annual_drawdown = df['daily_return'].resample('Y').apply(cal_max_drawdown)
    summary = pd.DataFrame({
    'Yearly Min Price': yearly_min,
    'Yearly Max Price': yearly_max,
    'Annual Return': annual_return,
    'Volatility': annual_volatility,
    'Sharpe Ratio': annual_sharpe,
    'Max Drawdown': annual_drawdown
    })
    summary.index = summary.index.year  # Clean up index
    for col in summary.columns:
        if col not in ['Yearly Max Price', 'Yearly Min Price','Sharpe Ratio']:
            summary[col] = summary[col].apply(lambda x: f"{x:.2%}" if isinstance(x, float) else x)
            
    # summary = summary.applymap(lambda x: f"{x:.2%}" if isinstance(x, float) else x)

    # Convert to HTML with centered text
    summary = html_table(summary.round(3).astype(str),index = True)
    def highlight_return(val):
        val = float(val.strip('%'))/100
        if isinstance(val, (int, float)):
            # Normalize intensity (adjust 0.2 to match your data range)
            intensity = min(abs(val) / 0.2, 1)
            if val > 0:
                # Green gradient: light to dark
                r = int(255 * (1 - intensity))
                g = 255
                b = int(255 * (1 - intensity))
            elif val < 0:
                # Red gradient: light to dark
                r = 255
                g = int(255 * (1 - intensity))
                b = int(255 * (1 - intensity))
            else:
                r, g, b = 255, 255, 255  # neutral
            return f'background-color: rgb({r}, {g}, {b})'
        return ''

    # styled = summary.style.applymap(highlight_return, subset=['Annual Return'])
    summary = summary.applymap(highlight_return, subset=['Annual Return'])

    # Display in Streamlit
    st.markdown("### Year-wise Performance Metrics")
    st.write(summary.to_html(escape=False), unsafe_allow_html=True)





else:
    st.warning("No stock price data found. Please visit the Live Chart page first.")



## use of page link
st.page_link("pages/01_LiveChart.py", label="Go to Live Chart")


