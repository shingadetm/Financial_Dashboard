from datetime import date

import pandas as pd
import streamlit as st

st.title("�� Stock Screener")


date_range = st.date_input(
    "Select a date range",
    value=(date(2020, 1, 1), date.today()),
    min_value=date(1900, 1, 1),
    max_value=date.today()
)

st.write("You selected:", date_range)

# Load your universe and apply filters
# df = pd.read_csv("your_stock_universe.csv")
# qualifying = df[df["PE Ratio"] < 15]
# st.dataframe(qualifying)


