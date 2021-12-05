from streamlit import columns as streamlit_columns


def setup_inputs():
    input_columns = streamlit_columns(4)

    depth = input_columns[0].number_input(
        'Insert desired depth',
        value=3,
        step=1)
    year = input_columns[1].number_input(
        "Year",
        value=2021,
        step=1)

    plot_all_years = input_columns[2].checkbox(
        "Plot all years")
    delta_percentage = input_columns[2].checkbox(
        "Delta in percentage")

    reg_degree = input_columns[3].number_input(
        "Regression degree",
        value=1,
        step=1,
        min_value=1,
        max_value=3)

    return depth, year, plot_all_years, delta_percentage, reg_degree
