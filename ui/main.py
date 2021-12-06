"""The generation of the UI.
"""
from const import SELECTBOX_HOME, SELECTBOX_INCOME_EXPENSE
from expenses import plot_expenses, plot_income
from inputs import setup_inputs
from metrics import get_assets_columns, add_metrics
from data_loader import load_data
from ploter import HistoricalPlot


import streamlit as st

selectbox = st.sidebar.selectbox(
    "Section",
    (SELECTBOX_HOME, SELECTBOX_INCOME_EXPENSE)
)

st.title('Cashboard')

depth, delta_percentage, reg_degree = setup_inputs()
assets, expenses, incomes = load_data(depth)
if selectbox == SELECTBOX_HOME:
    st.subheader('Assets')
    assets_columns = get_assets_columns(len(assets))
    balance_plot = HistoricalPlot("Balance")

    for col, asset in zip(assets_columns, assets):
        add_metrics(col, asset, delta_percentage)
        balance_plot.add_account_balance(asset)

    balance_plot.add_regression(reg_degree)

    balance_plot.plot()

elif selectbox == SELECTBOX_INCOME_EXPENSE:
    balance_plot = HistoricalPlot("Income and expenses")
    for income in incomes:
        balance_plot.add_account_diff(income, True)
    for expense in expenses:
        balance_plot.add_account_diff(expense, True)

    balance_plot.plot()

    # Expenses and incomes
    income_col, expenses_col = st.columns(2)

    income_col.plotly_chart(plot_expenses(expenses), use_container_width=True)
    expenses_col.plotly_chart(plot_income(incomes), use_container_width=True)
