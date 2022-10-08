"""The generation of the UI.
"""
from const import SELECTBOX_HOME, SELECTBOX_INCOME_EXPENSE, SELECTBOX_CUSTOM_QUERY
from expenses import plot_expenses, plot_income
from inputs import setup_inputs
from metrics import fill_metrics
from data_loader import load_data
from ploter import HistoricalPlot
from custom_query import render as custom_query_render

import streamlit as st

selectbox = st.sidebar.selectbox(
    "Section", (SELECTBOX_HOME, SELECTBOX_INCOME_EXPENSE, SELECTBOX_CUSTOM_QUERY)
)

st.title("Cashboard")

inputs = setup_inputs()

store = load_data(inputs.depth)
assets, expenses, incomes = store.assets, store.expenses, store.incomes

if selectbox == SELECTBOX_HOME:
    st.subheader("Assets")
    fill_metrics(assets, inputs.delta_percentage)
    balance_plot = HistoricalPlot("Balance")

    for asset in assets:
        balance_plot.add_account_balance(asset)

    balance_plot.add_regression(inputs.reg_degree, inputs.add_months_to_pred)

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

elif selectbox == SELECTBOX_CUSTOM_QUERY:
    custom_query_render(store)
