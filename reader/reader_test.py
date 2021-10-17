import pytest

from reader import CashStore

test_store = CashStore("testdata/my_cash.gnucash")

def test_get_accounts():
    assert len(test_store.accounts) > 0