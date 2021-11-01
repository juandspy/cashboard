import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd


from utils import load_data, pretty_currency, get_asset_delta, \
    daily_to_monthly, MONTHS

now = datetime.now()

st.title('Cashboard')

input_columns = st.columns(3)
depth = input_columns[0].number_input('Insert desired depth', value=1, step=1)
year = input_columns[1].number_input("Year", value=2021, step=1)
daily = input_columns[2].checkbox("Daily graph")
delta_percentage = input_columns[2].checkbox("Delta in percentage")

assets = load_data(depth)

st.subheader('Assets')
assets_columns = st.columns(len(assets))

st.subheader('Year gains')

fig = go.Figure()

for col, asset in zip(assets_columns, assets):
    # Fill metrics
    delta = float(get_asset_delta(asset, now.replace(month=now.month - 1 or 12).date())  )# TODO: cache
    if delta_percentage:
        delta = "{:.2f} %".format(delta/asset.balance*100)

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
    
    fig.add_trace(go.Bar(
        x=MONTHS,
        y=monthly_balance.iloc[
            monthly_balance.index.get_level_values('Year') == year],
        name=asset.name
    ))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='stack', xaxis_tickangle=-45)
st.plotly_chart(fig)