from reader.assets import Asset
from datetime import datetime

def get_asset_delta(asset: Asset, from_date: datetime.date) -> float:
    df_from_date = asset.split_df[asset.split_df['transaction.post_date'] >= from_date]
    return df_from_date["value"].sum()

def get_asset_balance_at_date(asset: Asset, from_date: datetime.date) -> float:
    df_until_date = asset.split_df[asset.split_df['transaction.post_date'] <= from_date]
    return df_until_date["value"].sum()