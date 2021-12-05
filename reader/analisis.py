import pandas as pd

from reader.accounts import CashAccount


def get_daily_delta(account: CashAccount) -> pd.DataFrame:
    df = account.split_df.copy()
    if df.empty: return pd.DataFrame()

    df["transaction.post_date"] = pd.to_datetime(df["transaction.post_date"])
    df['value'] = pd.to_numeric(df['value'],errors='coerce')
    return df.groupby('transaction.post_date')["value"].sum()


def get_daily_balance(account: CashAccount) -> pd.DataFrame:
    return get_daily_delta(account).cumsum()