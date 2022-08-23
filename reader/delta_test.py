import pytest
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from datetime import datetime, timedelta

from testdata.mocks import (
    mock_book,
    BANK_INITIAL_VALUE,
    CASH_INITIAL_VALUE,
    TRANSACTION_VALUE,
    transaction_date,
    opening_transaction_date,
)
from accounts import CashAccount
from cashstore import CashStore

from delta import get_account_delta, get_account_balance_at_date


mock_store = CashStore(book=mock_book)
mock_store.set_assets_depth(2)

bank_account = mock_store.assets[0]
cash_account = mock_store.assets[1]


def test_get_account_delta():
    # Delta from begging of time should be BANK_INITIAL_VALUE + TRANSACTION_VALUE for bank account
    assert (
        get_account_delta(bank_account, opening_transaction_date.date())  # bank account
        == BANK_INITIAL_VALUE - TRANSACTION_VALUE
    )
    # Delta from begging of time should be CASH_INITIAL_VALUE + TRANSACTION_VALUE for cash account
    assert (
        get_account_delta(cash_account, opening_transaction_date.date())  # cash account
        == CASH_INITIAL_VALUE + TRANSACTION_VALUE
    )

    # Delta from before the transaction should be -TRANSACTION_VALUE for bank account
    assert (
        get_account_delta(
            bank_account,  # bank account
            transaction_date.replace(day=transaction_date.day - 1).date(),
        )
        == -TRANSACTION_VALUE
    )
    # Delta from before the transaction should be TRANSACTION_VALUE for cash account
    assert (
        get_account_delta(
            cash_account,  # cash account
            transaction_date.replace(day=transaction_date.day - 1).date(),
        )
        == TRANSACTION_VALUE
    )


def test_get_account_balance_at_date():
    # Balance at the begging of time should be BANK_INITIAL_VALUE for bank account
    assert (
        get_account_balance_at_date(
            bank_account, opening_transaction_date.date()  # bank account
        )
        == BANK_INITIAL_VALUE
    )
    # Balance at the begging of time should be CASH_INITIAL_VALUE for cash account
    assert (
        get_account_balance_at_date(
            cash_account, opening_transaction_date.date()  # cash account
        )
        == CASH_INITIAL_VALUE
    )

    # Balance after the transaction should be BANK_INITIAL_VALUE-TRANSACTION_VALUE for bank account
    assert (
        get_account_balance_at_date(
            bank_account,  # bank account
            transaction_date.replace(day=transaction_date.day + 1).date(),
        )
        == BANK_INITIAL_VALUE - TRANSACTION_VALUE
    )
    # Balance after the transaction should be CASH_INITIAL_VALUE+TRANSACTION_VALUE for cash account
    assert (
        get_account_balance_at_date(
            cash_account,  # cash account
            transaction_date.replace(day=transaction_date.day + 1).date(),
        )
        == CASH_INITIAL_VALUE + TRANSACTION_VALUE
    )
