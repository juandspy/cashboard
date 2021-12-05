import streamlit as st


from utils import load_data
from metrics import get_assets_columns, add_metrics
from inputs import setup_inputs

st.title('Cashboard')

depth, year, plot_all_years, delta_percentage, reg_degree = setup_inputs()
assets, expenses = load_data(depth)

st.subheader('Assets')
assets_columns = get_assets_columns(len(assets))
for col, asset in zip(assets_columns, assets):
    add_metrics(col, asset, delta_percentage)

fig_gains = go.Figure()

total_monthly_balance = None
for col, asset in zip(assets_columns, assets):
    # Fill graph
    daily_balance = asset.get_daily_balance()
    monthly_balance = daily_to_monthly(daily_balance)
    if monthly_balance.empty: continue
    if total_monthly_balance is None:
        total_monthly_balance = monthly_balance.copy()
    else:
        total_monthly_balance = total_monthly_balance.add(monthly_balance, fill_value=0)
    if plot_all_years:
        fig_gains.add_trace(go.Bar(
            x=date_index_to_str(monthly_balance),
            y=monthly_balance.values,
            name=asset.name
        ))
    else:        
        fig_gains.add_trace(go.Bar(
            x=MONTHS,
            y=monthly_balance.iloc[
                monthly_balance.index.get_level_values('Year') == year],
            name=asset.name
        ))

# Remove zeros
total_monthly_balance_no_zeros = total_monthly_balance.loc[~(total_monthly_balance==0)]
if reg_degree == 1:
    y_pred = get_linear_regression(
        total_monthly_balance_no_zeros.index, 
        total_monthly_balance_no_zeros.values,
        total_monthly_balance.index)
else:
    y_pred = get_polynomial_regression(
        total_monthly_balance_no_zeros.index, 
        total_monthly_balance_no_zeros.values,
        total_monthly_balance.index,
        degree=reg_degree)

if plot_all_years:
    fig_gains.add_trace(go.Scatter(
        x=date_index_to_str(total_monthly_balance),
        y=y_pred
    ))
# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig_gains.update_layout(
    barmode='stack', 
    xaxis_tickangle=-45,
    title = "Year gains")

with st.expander("Year gains"):
    st.plotly_chart(fig_gains)

with st.expander("Year expenses"):
    from expenses import plot_expenses
    fig = plot_expenses(expenses)
    st.plotly_chart(fig)