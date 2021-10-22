import pytest

from reader import CashStore, get_assets_info

test_store = CashStore(
    # "testdata/my_cash.gnucash"
    "/home/jdiazsua/Documents/Personal/Finanzas/my_cash.gnucash")


def test_get_accounts():
    assert len(test_store.accounts) == 5

def test_get_assets_info():
    assert len(get_assets_info(test_store.book)) == 2