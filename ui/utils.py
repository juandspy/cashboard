import streamlit as st
import numpy as np
import pandas as pd
from datetime import date, timedelta
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from reader.cashstore import CashStore
from config.config_parser import parse_config

config = parse_config("config.toml")
N_CHART_POINTS = 12
NOISE_PERCENTAGE = 0.7
N_DELTA_DAYS = 30
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def get_account_delta(asset, from_date):
    from reader.delta import get_account_delta as gad
    return gad(asset, from_date)

# @st.cache
def load_data(depth: int = 1):
    print("Loading data", depth)
    store = CashStore(book_path=config.database)
    store.set_assets_depth(depth=depth)
    store.set_expenses_depth(depth=depth)
    
    return store.assets, store.expenses

def pretty_currency(currency: str) -> str:
    mapping = { 'EUR':'€', 'USD':'$'}
    currency = str(currency).split(":")[1][:-1]
    return mapping[currency] if currency in mapping.keys() else currency

def daily_to_monthly(df: pd.Series) -> pd.Series:
    if df.empty: return df
    # print(df)
    df = df.groupby([(df.index.year),(df.index.month)]).last()
    df.index.names = ["Year", "Month"]
    df = fill_dataframe(df)
    return df

def fill_dataframe(df: pd.Series) -> pd.Series:
    first_year, first_month = df.index[0]
    last_year, last_month = df.index[-1]

    value = 0
    for year in range(first_year, last_year+1):
        for month in range(1, 13):
            if (
                (year == first_year) & (month < first_month)
                ) | (
                    (year == last_year) & (month > last_month)):
                df.loc[year, month] = 0
            try:
                value = df.loc[year, month]
            except KeyError:
                df.loc[year, month] = value # set last value
                continue
    df = df.sort_index()
    return df


from typing import List
def date_index_to_str(df: pd.Series) -> List:
    return ["{}-{}".format(year, month) for (year, month) in df.index]