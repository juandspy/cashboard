"""The generation of the UI.
"""
from const import SELECTBOX_HOME, SELECTBOX_INCOME_EXPENSE, SELECTBOX_CUSTOM_QUERY
from expenses import plot_expenses, plot_income
from inputs import setup_inputs
from metrics import fill_metrics
from data_loader import load_data
from ploter import HistoricalPlot
import pandas as pd


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
    st.markdown(
        "Here you can run custom queries. Check the database schema [here](https://piecash.readthedocs.io/en/master/_images/schema.png)."
    )
    sql_query = st.text_area(
        "Write here your SQL query.",
        placeholder="SELECT name, account_type FROM accounts",
    )

    st.write("Some examples:")

    with st.expander("Aggregate all the transactions starting with 'CUSTOM_START'"):
        st.code(
            """
SELECT SUM(value_num)/100 FROM (

SELECT joined.value_num, t.description, t.post_date, t.enter_date
FROM
	(
		SELECT to_accounts.tx_guid, from_accounts.account_guid AS from_account, to_accounts.account_guid AS to_account, to_accounts.value_num
		FROM
		(
		SELECT tx_guid, account_guid, value_num
		FROM splits
		WHERE value_num > 0
		) AS to_accounts,
		(
		SELECT tx_guid, account_guid, value_num
		FROM splits
		WHERE value_num < 0
		) AS from_accounts
		WHERE to_accounts.tx_guid = from_accounts.tx_guid
	) AS joined, transactions as t
	WHERE t.guid = joined.tx_guid AND t.description LIKE "CUSTOM_START%"
)
        """
        )

    if sql_query:
        with st.spinner("Running SQL query"):
            results = store.run_sql(sql_query)

            parsed_results = []
            for row in results:
                parsed_results.append(row)
            df = pd.DataFrame(parsed_results, columns=results.keys())

            st.dataframe(df)
