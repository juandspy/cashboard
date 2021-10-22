import pytest

from reader import CashStore, get_assets

test_store = CashStore(
    # "testdata/my_cash.gnucash"
    "/home/jdiazsua/Documents/Personal/Finanzas/my_cash.gnucash")


def test_get_accounts():
    assert len(test_store.accounts) == 5

def test_get_assets():
    assert len(get_assets(test_store.book)) == 2