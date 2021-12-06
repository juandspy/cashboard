"""UI inputs.
"""
from streamlit import columns as streamlit_columns


def setup_inputs() -> (int, bool, int):
    """Place the inputs in the UI and returns its selected values.

    Returns:
        int, bool, int: depth; whether to show the delta as
        percentage or not; and the regression degree.
    """
    input_columns = streamlit_columns(3)

    depth = input_columns[0].number_input(
        'Insert desired depth',
        value=3,
        step=1)

    delta_percentage = input_columns[1].checkbox(
        "Delta in percentage")

    reg_degree = input_columns[2].number_input(
        "Regression degree",
        value=1,
        step=1,
        min_value=1,
        max_value=3)

    return depth, delta_percentage, reg_degree
