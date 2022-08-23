"""UI inputs.
"""
import streamlit as st


class Inputs:
    """All the user inputs used by this tool."""

    def __init__(self, depth, delta_percentage, add_months_to_pred, reg_degree):

        self.depth = depth
        self.delta_percentage = delta_percentage
        self.add_months_to_pred = add_months_to_pred
        self.reg_degree = reg_degree


def setup_inputs() -> Inputs:
    """Place the inputs in the UI and returns its selected values.

    Returns:
        int, bool, int: depth; whether to show the delta as
        percentage or not; and the regression degree.
    """
    sidebar = st.sidebar

    sidebar.markdown("""---""")

    depth = sidebar.number_input("Insert desired depth", value=3, step=1)

    add_months_to_pred = sidebar.number_input(
        "Add months to the regression", value=0, step=1, min_value=0, max_value=None
    )

    delta_percentage = sidebar.checkbox("Delta in percentage")

    reg_degree = sidebar.number_input(
        "Regression degree", value=1, step=1, min_value=1, max_value=3
    )

    return Inputs(depth, delta_percentage, int(add_months_to_pred), int(reg_degree))
