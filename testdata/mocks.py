import piecash
from piecash.core.factories import single_transaction
from decimal import Decimal
from datetime import datetime

TRANSACTION_VALUE = Decimal(100)
BANK_INITIAL_VALUE = 1000
BANK_ACCOUNT_NAME = "Account 1 bank sub account"
CASH_INITIAL_VALUE = 100
CASH_ACCOUNT_NAME = "Account 1 cash sub account"

MONTHS_AFTER_INITIAL_OPENING = 6

mock_book = piecash.create_book(currency="EUR")
EUR = mock_book.commodities.get(mnemonic="EUR")

opening_balance = piecash.Account(name="Opening Balance",
    type="EQUITY",
    parent=mock_book.root_account,
    commodity=EUR)

assets = piecash.Account(name="Assets",
    type="ASSET",
    parent=mock_book.root_account,
    commodity=EUR,
    placeholder=True,)

acc = piecash.Account(name="Current Assets",
    type="ASSET",
    parent=assets,
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

opening_balance_month = now.month - MONTHS_AFTER_INITIAL_OPENING
if opening_balance_month <= 0: opening_balance_month+=12
transaction_date = now.replace(month=opening_balance_month)
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