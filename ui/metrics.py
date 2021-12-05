import streamlit as st
from streamlit import columns as streamlit_columns

from const import METRICS_PER_ROW, now
from utils import get_account_delta, pretty_currency
from reader.accounts import CashAccount


def get_assets_columns(n_assets: int):
    assets_columns = None
    num_rows = round(n_assets / METRICS_PER_ROW)

    for row in range(num_rows):
        if assets_columns is None:
            assets_columns = st.columns(METRICS_PER_ROW)
        else:
            assets_columns += st.columns(METRICS_PER_ROW)

    if n_assets % METRICS_PER_ROW != 0:
        assets_columns += st.columns(n_assets % METRICS_PER_ROW)
    return assets_columns


def add_metrics(col: streamlit_columns, account: CashAccount, delta_percentage=False):
    last_month_date = now.replace(month=now.month - 1 or 12).date()
    delta = float(get_account_delta(account, last_month_date))
    if delta == 0:
        delta = None
    else:
        if delta_percentage:
            delta = "{:.2f} %".format(delta/account.current_balance*100)

    if delta == 0:
        delta = None

    col.metric(
        account.name,
        "{} {}".format(
            account.current_balance,
            pretty_currency(account.currency)),
        delta)
