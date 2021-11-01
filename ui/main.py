import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd


from utils import load_data, pretty_currency, get_asset_delta, \
    daily_to_monthly, MONTHS, date_index_to_str
from predictions import get_linear_regression, get_polynomial_regression


now = datetime.now()

st.title('Cashboard')

input_columns = st.columns(3)
depth = input_columns[0].number_input('Insert desired depth', value=1, step=1)
year = input_columns[1].number_input("Year", value=2021, step=1)
plot_all_years = input_columns[2].checkbox("Plot all years")
delta_percentage = input_columns[2].checkbox("Delta in percentage")
reg_degree = input_columns[2].number_input(
    "Regression degree", value=1, step=1, min_value=1, max_value=3)

assets = load_data(depth)

st.subheader('Assets')
assets_columns = st.columns(len(assets))

st.subheader('Year gains')

fig = go.Figure()

total_monthly_balance = None
for col, asset in zip(assets_columns, assets):
    # Fill metrics
    delta = float(get_asset_delta(asset, now.replace(month=now.month - 1 or 12).date())  )# TODO: cache
    if delta_percentage:
        if delta != 0:
            delta = "{:.2f} %".format(delta/asset.current_balance*100)

    if delta == 0:
        delta = None

    col.metric(
        asset.name, 
        "{} {}".format(
            asset.current_balance, 
            pretty_currency(asset.currency)),
        delta)
    
    # Fill graph
    daily_balance = asset.get_daily_balance()
    monthly_balance = daily_to_monthly(daily_balance)
    if monthly_balance.empty: continue
    if total_monthly_balance is None:
        total_monthly_balance = monthly_balance.copy()
    else:
        total_monthly_balance = total_monthly_balance.add(monthly_balance, fill_value=0)
    if plot_all_years:
        fig.add_trace(go.Bar(
            x=date_index_to_str(monthly_balance),
            y=monthly_balance.values,
            name=asset.name
        ))
    else:        
        fig.add_trace(go.Bar(
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
    fig.add_trace(go.Scatter(
        x=date_index_to_str(total_monthly_balance),
        y=y_pred
    ))
# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='stack', xaxis_tickangle=-45)
st.plotly_chart(fig)