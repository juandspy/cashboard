import pytest
import piecash
from piecash.core.factories import single_transaction
from decimal import Decimal
from datetime import datetime, timedelta

from reader import CashStore, get_assets, get_asset_delta


TRANSACTION_VALUE = Decimal(100)
NUMBER_OF_TRANSACTONS = 3
BANK_INITIAL_VALUE = 1000
BANK_ACCOUNT_NAME = "Account 1 bank sub account"
CASH_INITIAL_VALUE = 100
CASH_ACCOUNT_NAME = "Account 1 cash sub account"

mock_book = piecash.create_book(currency="EUR")
EUR = mock_book.commodities.get(mnemonic="EUR")

opening_balance = piecash.Account(name="Opening Balance",
    type="EQUITY",
    parent=mock_book.root_account,
    commodity=EUR)

acc = piecash.Account(name="Account 1",
    type="ASSET",
    parent=mock_book.root_account,
    commodity=EUR,
    placeholder=True,)

bank = piecash.Account(name=BANK_ACCOUNT_NAME,
    type="BANK",
    parent=acc,
    commodity=EUR,
    commodity_scu=BANK_INITIAL_VALUE,
    description="my bank account",
    code="BANK1",)

cash = piecash.Account(name=CASH_ACCOUNT_NAME,
    type="CASH",
    parent=acc,
    commodity=EUR,
    commodity_scu=CASH_INITIAL_VALUE,
    description="my cash in wallet",
    code="CASH1",)

now = datetime.now()

transaction_date = now.replace(month=now.month - 1 or 12)
for (acc, balance) in zip ([bank, cash], [BANK_INITIAL_VALUE, CASH_INITIAL_VALUE]):
    single_transaction(
        post_date=transaction_date.date(),
        enter_date=transaction_date,
        description="a month ago balance",
        value=balance,
        from_account=opening_balance,
        to_account=acc)

transaction_date = now.replace(day=now.day - 1)
single_transaction(
    post_date=transaction_date.date(),
    enter_date=transaction_date,
    description="yesterday withdrawal from bank to cash",
    value=TRANSACTION_VALUE,
    from_account=bank,
    to_account=cash)
 
mock_book.flush()

mock_book.save()
mock_store = CashStore(book=mock_book)


def test_get_accounts():
    assert len(mock_store.accounts) == 2

def test_get_assets():
    assets = get_assets(mock_store.book)
    assert len(assets) == 2
    assert "Account 1 bank sub account" == assets[0].name
    assert BANK_INITIAL_VALUE - TRANSACTION_VALUE == assets[0].balance
    assert "Account 1 cash sub account" == assets[1].name
    assert CASH_INITIAL_VALUE + TRANSACTION_VALUE == assets[1].balance

def test_get_asset_delta():
    assets = get_assets(mock_store.book)
    assert get_asset_delta(mock_store.book, assets[0].account, 5) == -TRANSACTION_VALUE
    assert get_asset_delta(mock_store.book, assets[1].account, 5) == TRANSACTION_VALUE