import streamlit as st
import pandas as pd

from const import SQL_QUERY__CUSTOM_START


def render(store):
    """Renders the custom query page."""

    st.markdown(
        "Here you can run custom queries."
        + "Check the database schema [here](https://piecash.readthedocs.io/en/master/_images/schema.png)."
    )

    sql_query = st.text_area(
        "Write here your SQL query.",
        placeholder="SELECT name, account_type FROM accounts",
    )

    st.write("Some examples:")

    with st.expander("Aggregate all the transactions starting with 'CUSTOM_START'"):
        st.code(SQL_QUERY__CUSTOM_START)

    if sql_query:
        with st.spinner("Running SQL query"):
            results = store.run_sql(sql_query)

            parsed_results = []
            for row in results:
                parsed_results.append(row)
            df = pd.DataFrame(parsed_results, columns=results.keys())

            st.dataframe(df)
