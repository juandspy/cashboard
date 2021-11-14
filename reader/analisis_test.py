import pytest
import pandas as pd
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from testdata.mocks import mock_book, transaction_date, opening_transaction_date, BANK_INITIAL_VALUE, TRANSACTION_VALUE
from cashstore import CashStore

mock_store = CashStore(book=mock_book)
mock_store.set_assets_depth(1)
bank_account = mock_store.assets[0]

def test_get_daily_delta():
    from analisis import get_daily_delta

    got_df = get_daily_delta(bank_account)

    assert got_df[
        pd.Timestamp(opening_transaction_date.date())] == BANK_INITIAL_VALUE
    assert got_df[
        pd.Timestamp(transaction_date.date())] == -TRANSACTION_VALUE

def test_get_daily_balance():
    from analisis import get_daily_balance

    got_df = get_daily_balance(bank_account)
    assert got_df[
        pd.Timestamp(opening_transaction_date.date())] == BANK_INITIAL_VALUE
    assert got_df[
        pd.Timestamp(transaction_date.date())] == BANK_INITIAL_VALUE-TRANSACTION_VALUE