import pandas as pd

from reader.assets import Asset


def get_daily_delta(asset: Asset) -> pd.DataFrame:
    df = asset.split_df.copy()
    if df.empty: return pd.DataFrame()

    df["transaction.post_date"] = pd.to_datetime(df["transaction.post_date"])
    df['value'] = pd.to_numeric(df['value'],errors='coerce')
    return df.groupby('transaction.post_date')["value"].sum()


def get_daily_balance(asset: Asset) -> pd.DataFrame:
    df = asset.split_df.copy()
    if df.empty: return pd.DataFrame()

    return get_daily_delta(asset).cumsum()