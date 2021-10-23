import streamlit as st
from datetime import datetime
import numpy as np

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../reader"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../testdata"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../config"))
from mocks import mock_book, TRANSACTION_VALUE, BANK_INITIAL_VALUE, BANK_ACCOUNT_NAME, CASH_INITIAL_VALUE, CASH_ACCOUNT_NAME
from reader import CashStore, get_assets
from config_parser import parse_config

config = parse_config("config.toml")
N_CHART_POINTS = 12
NOISE_PERCENTAGE = 0.7
N_DELTA_DAYS = 30

# @st.cache
def load_data():
    print("ok")
    now = datetime.now()
    store = CashStore(book_path=config.database)

    assets = get_assets(store.book, depth=1)
    for asset in assets:
        asset.set_delta(now.replace(month=now.month - 1 or 12))
    return assets

def pretty_currency(currency: str) -> str:
    mapping = { 'EUR':'€', 'USD':'$'}
    currency = str(currency).split(":")[1][:-1]
    return mapping[currency] if currency in mapping.keys() else currency
