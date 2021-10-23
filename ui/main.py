import streamlit as st
import plotly.graph_objects as go

from utils import load_data, pretty_currency


MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

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
    if delta_percentage:
        asset_delta = "{:.2f} %".format(asset.delta/asset.balance*100)
    else:
        asset_delta = asset.delta
    if asset.delta == 0:
        asset_delta = None

    col.metric(
        asset.name, 
        "{} {}".format(
            asset.balance, 
            pretty_currency(asset.currency)),
        asset_delta)
    
    # Fill graph
    fig.add_trace(go.Bar(
        x=MONTHS,
        y=asset.get_monthly_data(),
        name=asset.name
    ))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='stack', xaxis_tickangle=-45)
st.plotly_chart(fig)