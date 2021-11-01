import pytest
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from testdata.mocks import mock_book, CURRENT_ASSETS_NAME, BANK_ACCOUNT_NAME, CASH_ACCOUNT_NAME, BANK_SUB_ACCOUNT_1_NAME, BANK_SUB_ACCOUNT_2_NAME
from cashstore import CashStore

mock_store = CashStore(book=mock_book)

accounts_to_account_names = lambda list_x: [x.name for x in list_x] # just a test helper

def test_get_asset_children():
    from piecash import Account
    from assets import get_asset_children
    assets_account = mock_store.book.get(Account, name="Assets", parent=mock_store.book.root_account)
    
    # if current depth is depth, it should return an empty list
    assert get_asset_children(assets_account, 1, 1) == [] 
    # if current depth higher than depth, it should return an empty list
    assert get_asset_children(assets_account, 1, 0) == [] 
    # if current depth differs in 1 unit to desired depth, just the first children account is returned (current assets)
    assert accounts_to_account_names(get_asset_children(assets_account, 0, 1)) == [CURRENT_ASSETS_NAME]
    # if current depth differs in 2 units to desired depth, Current Assets immediate children are returned
    assert accounts_to_account_names(get_asset_children(assets_account, 0, 2)) == [BANK_ACCOUNT_NAME, CASH_ACCOUNT_NAME]
    # if current depth differs in 3 units Current Assets' children's children are returned
    assert accounts_to_account_names(get_asset_children(assets_account, 0, 3)) == [BANK_SUB_ACCOUNT_1_NAME, BANK_SUB_ACCOUNT_2_NAME, CASH_ACCOUNT_NAME]

def test_get_book_assets():
    from assets import get_book_assets

    assert accounts_to_account_names(get_book_assets(mock_store.book, depth=0))  == []
    assert accounts_to_account_names(get_book_assets(mock_store.book, depth=1))  == [BANK_ACCOUNT_NAME, CASH_ACCOUNT_NAME]
    assert accounts_to_account_names(get_book_assets(mock_store.book, depth=2)) == [BANK_SUB_ACCOUNT_1_NAME, BANK_SUB_ACCOUNT_2_NAME, CASH_ACCOUNT_NAME]

def test_get_daily_balance():
    mock_store.set_assets_depth(1)
    bank_account = mock_store.assets[0]

    assert not bank_account.get_daily_balance().empty