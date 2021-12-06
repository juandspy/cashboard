"""
Some useful functions.
"""
from typing import List
import pandas as pd


def pretty_currency(currency: str) -> str:
    """Returns the currency pretty printed. For example:
        Commodity<CURRENCY:EUR>
    is parsed as
        €

    Args:
        currency (str): the piecash currency.

    Returns:
        str: the currency simbol.
    """
    mapping = {'EUR': '€', 'USD': '$'}
    currency = str(currency).split(":")[1][:-1]
    return mapping[currency] if currency in mapping else currency


def daily_to_monthly(df: pd.Series) -> pd.Series:
    """Groups a daily series into a monthly one.

    Args:
        df (pd.Series): the daily series.

    Returns:
        pd.Series: the series grouped by month and year.
    """
    if df.empty:
        return df
    df = df.groupby([(df.index.year), (df.index.month)]).last()
    df.index.names = ["Year", "Month"]
    df = fill_series(df)
    return df


def fill_series(df: pd.Series) -> pd.Series:
    """Fill a pandas monthly series with zeros in case the month
    and year doesn't exist.

    Args:
        df (pd.Series): the monthly series.

    Returns:
        pd.Series: the filled series.
    """
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
                df.loc[year, month] = value  # set last value
                continue
    df = df.sort_index()
    return df


def date_index_to_str(df: pd.Series) -> List:
    """Converts the pandas series' index into a list of $MONTH-$YEAR.

    Args:
        df (pd.Series): the series.

    Returns:
        List: the list of $MONTH-$YEAR data.
    """
    return [f"{year}-{month}" for (year, month) in df.index]
