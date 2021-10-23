import pytest
import piecash
from datetime import datetime, timedelta

now = datetime.now()

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../testdata"))
from mocks import mock_book, TRANSACTION_VALUE, BANK_INITIAL_VALUE, BANK_ACCOUNT_NAME, CASH_INITIAL_VALUE, CASH_ACCOUNT_NAME, MONTHS_AFTER_INITIAL_OPENING, opening_balance_month

from reader import CashStore, get_assets, get_asset_delta, get_asset_balance_at_date

mock_store = CashStore(book=mock_book)


def test_get_accounts():
    assert len(mock_store.accounts) == 2

def test_get_assets():
    assets = get_assets(mock_store.book)
    assert len(assets) == 2
    assert BANK_ACCOUNT_NAME == assets[0].name
    assert BANK_INITIAL_VALUE - TRANSACTION_VALUE == assets[0].balance
    assert CASH_ACCOUNT_NAME == assets[1].name
    assert CASH_INITIAL_VALUE + TRANSACTION_VALUE == assets[1].balance

def test_get_asset_delta():
    assets = get_assets(mock_store.book)
    assert get_asset_delta(assets[0].account, now.replace(day=now.day - 5)) == -TRANSACTION_VALUE
    assert get_asset_delta(assets[1].account, now.replace(day=now.day - 5)) == TRANSACTION_VALUE

def test_get_asset_date_balance():
    assets = get_assets(mock_store.book)
    assert get_asset_balance_at_date(assets[0].account, now.replace(year=now.year - 5)) == 0
    assert get_asset_balance_at_date(assets[0].account, now.replace(day=now.day - 5)) == BANK_INITIAL_VALUE
    assert get_asset_balance_at_date(assets[0].account, now) == BANK_INITIAL_VALUE-TRANSACTION_VALUE

    assert get_asset_balance_at_date(assets[1].account, now.replace(year=now.year - 5)) == 0
    assert get_asset_balance_at_date(assets[1].account, now.replace(day=now.day - 5)) == CASH_INITIAL_VALUE
    assert get_asset_balance_at_date(assets[1].account, now) == CASH_INITIAL_VALUE+TRANSACTION_VALUE

def test_get_monthly_data(): # TODO: add the cash one
    transaction_month = now.replace(day=now.day - 5).month
    EXPECTED_BANK_MONTHLY_DATA = [0 for i in range(12)]
    EXPECTED_CASH_MONTHLY_DATA = [0 for i in range(12)]

    for i in range(12):
        if (i >= opening_balance_month - 1) & (i <= transaction_month - 1):
            EXPECTED_BANK_MONTHLY_DATA[i] = BANK_INITIAL_VALUE
            EXPECTED_CASH_MONTHLY_DATA[i] = CASH_INITIAL_VALUE
        else:
            EXPECTED_BANK_MONTHLY_DATA[i] = 0
            EXPECTED_CASH_MONTHLY_DATA[i] = 0
        if i == transaction_month - 1:
            EXPECTED_BANK_MONTHLY_DATA[i] -= TRANSACTION_VALUE
            EXPECTED_CASH_MONTHLY_DATA[i] += TRANSACTION_VALUE

    assets = get_assets(mock_store.book)
    assert len(assets) == 2
    assert EXPECTED_BANK_MONTHLY_DATA == assets[0].get_monthly_data()
    assert EXPECTED_CASH_MONTHLY_DATA == assets[1].get_monthly_data()