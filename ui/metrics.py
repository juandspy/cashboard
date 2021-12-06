"""Fills the values for the metrics about the assets current balance.
"""
import streamlit as st
from streamlit import columns as streamlit_columns

from const import METRICS_PER_ROW, now
from utils import pretty_currency
from reader.accounts import CashAccount
from reader.delta import get_account_delta


def get_assets_columns(n_assets: int) -> streamlit_columns:
    """Generate the rows and columns where the assets balance will
    be placed.

    Args:
        n_assets (int): number of assets.

    Returns:
        streamlit.columns: streamlit columns.
    """
    assets_columns = None
    num_rows = round(n_assets / METRICS_PER_ROW)

    for _ in range(num_rows):
        if assets_columns is None:
            assets_columns = st.columns(METRICS_PER_ROW)
        else:
            assets_columns += st.columns(METRICS_PER_ROW)

    if n_assets % METRICS_PER_ROW != 0:
        assets_columns += st.columns(n_assets % METRICS_PER_ROW)
    return assets_columns


def add_metrics(col: streamlit_columns, account: CashAccount, delta_percentage=False):
    """Fill the metrics with the accounts data.

    Args:
        col (streamlit.columns): the streamlit column to fill.
        account (CashAccount): the account.
        delta_percentage (bool, optional): Whether to show the delta as percentage or
        absolute value. Defaults to False.
    """
    last_month_date = now.replace(month=now.month - 1 or 12).date()
    delta = float(get_account_delta(account, last_month_date))
    if delta == 0:
        delta = None
    else:
        if delta_percentage:
            delta = f"{delta/account.current_balance*100:.2f} %"

    if delta == 0:
        delta = None

    col.metric(
        account.name,
        f"{account.current_balance} {pretty_currency(account.currency)}",
        delta)
