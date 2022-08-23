from accounts import get_book_accounts_of_type
from cashstore import CashStore
from testdata.mocks import mock_book
from testdata.const import (
    CURRENT_ASSETS_NAME,
    BANK_ACCOUNT_NAME,
    CASH_ACCOUNT_NAME,
    BANK_SUB_ACCOUNT_1_NAME,
    BANK_SUB_ACCOUNT_2_NAME,
    GAS_EXPENSES_NAME,
    ASSETS_NAME,
    CAR_EXPENSES_NAME,
    EXPENSES_NAME,
    EMPTY_ASSETS_NAME,
)
import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))


mock_store = CashStore(book=mock_book)


def accounts_to_account_names(list_x):
    return [x.name for x in list_x]  # just a test helper


def accounts_to_account_parents(list_x):
    return [x.parent for x in list_x]  # just a test helper


def test_get_account_children():
    from piecash import Account
    from accounts import get_account_children

    book_assets = mock_store.book.get(
        Account, name="Assets", parent=mock_store.book.root_account
    )

    # if current depth is depth, it should return an empty list
    assert get_account_children(book_assets, 1, 1) == []
    # if current depth higher than depth, it should return an empty list
    assert get_account_children(book_assets, 1, 0) == []

    # if current depth differs in 1 unit to desired depth, just the first children account is returned (current assets)
    sub_accounts = get_account_children(book_assets, 0, 1)
    assert accounts_to_account_names(sub_accounts) == [CURRENT_ASSETS_NAME]
    assert accounts_to_account_parents(sub_accounts) == [ASSETS_NAME]
    # if current depth differs in 2 units to desired depth, Current Assets immediate children are returned
    sub_accounts = get_account_children(book_assets, 0, 2)
    assert accounts_to_account_names(sub_accounts) == [
        BANK_ACCOUNT_NAME,
        CASH_ACCOUNT_NAME,
        EMPTY_ASSETS_NAME,
    ]
    assert accounts_to_account_parents(sub_accounts) == [CURRENT_ASSETS_NAME] * 3
    # if current depth differs in 3 units Current Assets' children's children are returned
    sub_accounts = get_account_children(book_assets, 0, 3)
    assert accounts_to_account_names(sub_accounts) == [
        BANK_SUB_ACCOUNT_1_NAME,
        BANK_SUB_ACCOUNT_2_NAME,
        CASH_ACCOUNT_NAME,
        EMPTY_ASSETS_NAME,
    ]
    assert accounts_to_account_parents(sub_accounts) == [
        BANK_ACCOUNT_NAME,
        BANK_ACCOUNT_NAME,
        CURRENT_ASSETS_NAME,
        CURRENT_ASSETS_NAME,
    ]


def test_get_book_assets():
    assets = get_book_accounts_of_type("ASSET", mock_store.book, depth=0)
    assert accounts_to_account_names(assets) == []

    assets = get_book_accounts_of_type("ASSET", mock_store.book, depth=1)
    assert accounts_to_account_names(assets) == [CURRENT_ASSETS_NAME]
    assert accounts_to_account_parents(assets) == [ASSETS_NAME]

    assets = get_book_accounts_of_type("ASSET", mock_store.book, depth=2)
    assert accounts_to_account_names(assets) == [
        BANK_ACCOUNT_NAME,
        CASH_ACCOUNT_NAME,
        EMPTY_ASSETS_NAME,
    ]
    assert accounts_to_account_parents(assets) == [CURRENT_ASSETS_NAME] * 3

    assets = get_book_accounts_of_type("ASSET", mock_store.book, depth=3)
    assert accounts_to_account_names(assets) == [
        BANK_SUB_ACCOUNT_1_NAME,
        BANK_SUB_ACCOUNT_2_NAME,
        CASH_ACCOUNT_NAME,
        EMPTY_ASSETS_NAME,
    ]
    assert accounts_to_account_parents(assets) == [
        BANK_ACCOUNT_NAME,
        BANK_ACCOUNT_NAME,
        CURRENT_ASSETS_NAME,
        CURRENT_ASSETS_NAME,
    ]


def test_get_book_expenses():
    expenses = get_book_accounts_of_type("EXPENSE", mock_store.book, depth=0)
    assert accounts_to_account_names(expenses) == []
    assert accounts_to_account_parents(expenses) == []

    expenses = get_book_accounts_of_type("EXPENSE", mock_store.book, depth=1)
    assert accounts_to_account_names(expenses) == [CAR_EXPENSES_NAME]
    assert accounts_to_account_parents(expenses) == [EXPENSES_NAME]

    expenses = get_book_accounts_of_type("EXPENSE", mock_store.book, depth=2)
    assert accounts_to_account_names(expenses) == [GAS_EXPENSES_NAME]
    assert accounts_to_account_parents(expenses) == [CAR_EXPENSES_NAME]


def test_get_book_incomes():
    # TODO:
    pass


def test_get_daily_balance():
    mock_store.set_assets_depth(2)
    bank_account = mock_store.assets[0]

    assert not bank_account.get_daily_balance().empty
