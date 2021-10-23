import streamlit as st
import plotly.graph_objects as go

from utils import load_data, pretty_currency


MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

st.title('Cashboard')
depth = st.number_input('Insert desired depth', value=1, step=1)
assets = load_data(depth)

st.subheader('Assets')
assets_columns = st.columns(len(assets))

fig = go.Figure()

for col, asset in zip(assets_columns, assets):
    # Fill metrics
    col.metric(
        asset.name, 
        "{} {}".format(
            asset.balance, 
            pretty_currency(asset.currency)),
        asset.delta)
    
    # Fill graph
    fig.add_trace(go.Bar(
        x=MONTHS,
        y=asset.get_monthly_data(),
        name=asset.name
    ))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='stack', xaxis_tickangle=-45)

st.subheader('Year gains')
st.plotly_chart(fig)