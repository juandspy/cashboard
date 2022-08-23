"""Fills the values for the metrics about the assets current balance.
"""
import streamlit as st
from streamlit import columns as streamlit_columns

from const import METRICS_PER_ROW, now
from ui_utils import pretty_currency
from reader.accounts import CashAccount
from reader.delta import get_account_delta


def get_assets_columns(n_assets: int, hidden=False) -> streamlit_columns:
    """Generate the rows and columns where the assets balance will
    be placed.

    Args:
        n_assets (int): number of assets.

    Returns:
        streamlit.columns: streamlit columns.
    """
    assets_columns = None
    if METRICS_PER_ROW <= n_assets:
        num_rows = round(n_assets / METRICS_PER_ROW)
    else:
        num_rows = n_assets

    if hidden:
        container = st.expander("Non active assets:")
    else:
        container = st

    for _ in range(num_rows):
        if assets_columns is None:
            assets_columns = container.columns(METRICS_PER_ROW)
        else:
            assets_columns += container.columns(METRICS_PER_ROW)

    if n_assets % METRICS_PER_ROW != 0:
        # Add the last row
        assets_columns += container.columns(n_assets % METRICS_PER_ROW)
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
        delta,
    )


def fill_metrics(assets, delta_percentage):
    non_empty_assets = [asset for asset in assets if asset.current_balance != 0]
    empty_assets = [asset for asset in assets if asset.current_balance == 0]

    non_empty_assets_columns = get_assets_columns(len(non_empty_assets))
    empty_assets_columns = get_assets_columns(len(empty_assets), True)

    for col, asset in zip(non_empty_assets_columns, non_empty_assets):
        add_metrics(col, asset, delta_percentage)

    for col, asset in zip(empty_assets_columns, empty_assets):
        add_metrics(col, asset, delta_percentage)
