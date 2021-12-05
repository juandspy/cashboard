from inputs import setup_inputs
from metrics import get_assets_columns, add_metrics
from utils import load_data
from ploter import HistoricalPlot

import streamlit as st

st.title('Cashboard')

depth, delta_percentage, reg_degree = setup_inputs()
assets, expenses = load_data(depth)

st.subheader('Assets')
assets_columns = get_assets_columns(len(assets))
balance_plot = HistoricalPlot("Balance")

for col, asset in zip(assets_columns, assets):
    add_metrics(col, asset, delta_percentage)
    balance_plot.add_account(asset)

balance_plot.add_regression(reg_degree)

balance_plot.plot()

# with st.expander("Year expenses"):
#     from expenses import plot_expenses
#     fig = plot_expenses(expenses)
#     st.plotly_chart(fig)
