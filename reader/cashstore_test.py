import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from testdata.mocks import mock_book, BANK_ACCOUNT_NAME, CASH_ACCOUNT_NAME, OPENING_BALANCE_NAME, \
    ASSETS_NAME, BANK_SUB_ACCOUNT_1_NAME, BANK_SUB_ACCOUNT_2_NAME
from cashstore import CashStore


mock_store = CashStore(book=mock_book)

def test_CashStore_accounts():
    got_accounts = []
    for acc in mock_store.accounts:
        got_accounts.append(acc.name)
    assert got_accounts == [OPENING_BALANCE_NAME, ASSETS_NAME]

def test_CashStore_assets():
    assert mock_store.assets == []
    mock_store.set_assets_depth(1)
    assert len(mock_store.assets) == len([BANK_ACCOUNT_NAME, CASH_ACCOUNT_NAME])
    mock_store.set_assets_depth(2)
    assert len(mock_store.assets) == len([BANK_SUB_ACCOUNT_1_NAME, BANK_SUB_ACCOUNT_2_NAME, CASH_ACCOUNT_NAME])

def test_CashStore_update_assets_splits():
    mock_store.set_assets_depth(1)
    assert not mock_store.assets[0].split_df.empty