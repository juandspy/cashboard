from testdata.mocks import mock_book
from cashstore import CashStore
from testdata.const import (
    BANK_ACCOUNT_NAME,
    CASH_ACCOUNT_NAME,
    OPENING_BALANCE_NAME,
    ASSETS_NAME,
    BANK_SUB_ACCOUNT_1_NAME,
    BANK_SUB_ACCOUNT_2_NAME,
    EXPENSES_NAME,
    EMPTY_ASSETS_NAME,
    INCOMES_NAME,
)
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))


mock_store = CashStore(book=mock_book)


def test_CashStore_accounts():
    got_accounts = []
    for acc in mock_store.accounts:
        got_accounts.append(acc.name)
    assert got_accounts == [
        OPENING_BALANCE_NAME,
        ASSETS_NAME,
        EXPENSES_NAME,
        INCOMES_NAME,
    ]


def test_CashStore_assets():
    assert mock_store.assets == []
    mock_store.set_assets_depth(1)
    assert len(mock_store.assets) == len([ASSETS_NAME])

    mock_store.set_assets_depth(2)
    assert len(mock_store.assets) == len(
        [BANK_ACCOUNT_NAME, CASH_ACCOUNT_NAME, EMPTY_ASSETS_NAME]
    )

    mock_store.set_assets_depth(3)
    assert len(mock_store.assets) == len(
        [
            BANK_SUB_ACCOUNT_1_NAME,
            BANK_SUB_ACCOUNT_2_NAME,
            CASH_ACCOUNT_NAME,
            EMPTY_ASSETS_NAME,
        ]
    )


def test_CashStore_update_assets_splits():
    mock_store.set_assets_depth(1)
    assert mock_store.assets[0].split_df.empty
    mock_store.set_assets_depth(2)
    assert not mock_store.assets[0].split_df.empty
