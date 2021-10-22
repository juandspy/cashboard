import pytest
import piecash

from reader import CashStore, get_assets


mock_book = piecash.create_book(currency="EUR")
EUR = mock_book.commodities.get(mnemonic="EUR")

acc = piecash.Account(name="Account 1",
    type="ASSET",
    parent=mock_book.root_account,
    commodity=EUR,
    placeholder=True,)

piecash.Account(name="Account 1 bank sub account",
    type="BANK",
    parent=acc,
    commodity=EUR,
    commodity_scu=1000,
    description="my bank account",
    code="BANK1",)

piecash.Account(name="Account 1 cash sub account",
    type="CASH",
    parent=acc,
    commodity=EUR,
    commodity_scu=1000,
    description="my cash in wallet",
    code="CASH1",)

mock_book.save()
mock_store = CashStore(book=mock_book)


def test_get_accounts():
    assert len(mock_store.accounts) == 1

def test_get_assets():
    assert len(get_assets(mock_store.book)) == 2