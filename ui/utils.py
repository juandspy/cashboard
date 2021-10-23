import streamlit as st
from datetime import datetime
import numpy as np

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../reader"))

from reader import CashStore, get_assets

N_CHART_POINTS = 12
NOISE_PERCENTAGE = 0.7
N_DELTA_DAYS = 30

# @st.cache
def load_data():
    print("ok")
    now = datetime.now()
    store = CashStore(book_path="testdata/my_cash.gnucash")

    assets = get_assets(store.book)
    for asset in assets:
        asset.set_delta(now.replace(month=now.month - 1 or 12))
    return assets