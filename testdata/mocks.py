import piecash
from piecash.core.factories import single_transaction
from datetime import datetime

BANK_ACCOUNT_NAME = "Bank account"
BANK_SUB_ACCOUNT_1_NAME = "Bank account 1"
BANK_SUB_ACCOUNT_2_NAME = "Bank account 2"
OPENING_BALANCE_NAME = "Opening Balance"
ASSETS_NAME = "Assets"
CURRENT_ASSETS_NAME = "Current Assets"
CASH_ACCOUNT_NAME = "Cash account"

EXPENSES_NAME="Expenses"
CAR_EXPENSES_NAME="Car"

TRANSACTION_VALUE = 100
BANK_INITIAL_VALUE = 1000
CASH_INITIAL_VALUE = 100

MONTHS_AFTER_INITIAL_OPENING = 6

mock_book = piecash.create_book(currency="EUR")
EUR = mock_book.commodities.get(mnemonic="EUR")

now = datetime.now()

opening_balance_month = now.month - MONTHS_AFTER_INITIAL_OPENING
if opening_balance_month <= 0: opening_balance_month+=12
opening_transaction_date = now.replace(month=opening_balance_month)

transaction_date = now.replace(day=now.day - 1)

opening_balance = piecash.Account(name=OPENING_BALANCE_NAME,
    type="EQUITY",
    parent=mock_book.root_account,
    commodity=EUR)

assets = piecash.Account(name=ASSETS_NAME,
    type="ASSET",
    parent=mock_book.root_account,
    commodity=EUR,
    placeholder=True,)

acc = piecash.Account(name=CURRENT_ASSETS_NAME,
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

sub_bank_1 = piecash.Account(name=BANK_SUB_ACCOUNT_1_NAME,
    type="BANK",
    parent=bank,
    commodity=EUR,
    commodity_scu=BANK_INITIAL_VALUE,
    description="my bank subaccount 1",
    code="BANK1_1",)

sub_bank_2 = piecash.Account(name=BANK_SUB_ACCOUNT_2_NAME,
    type="BANK",
    parent=bank,
    commodity=EUR,
    commodity_scu=0,
    description="my bank subaccount 2",
    code="BANK1_2",)

cash = piecash.Account(name=CASH_ACCOUNT_NAME,
    type="CASH",
    parent=acc,
    commodity=EUR,
    commodity_scu=CASH_INITIAL_VALUE,
    description="my cash in wallet",
    code="CASH1",)

expenses = piecash.Account(name=EXPENSES_NAME,
    type="EXPENSE",
    parent=mock_book.root_account,
    commodity=EUR,
    placeholder=True,)

car = piecash.Account(name=CAR_EXPENSES_NAME,
    type="EXPENSE",
    parent=expenses,
    commodity=EUR,
    description="car expenses",
    code="CAR",)

for (acc, balance) in zip ([bank, cash], [BANK_INITIAL_VALUE, CASH_INITIAL_VALUE]):
    single_transaction(
        post_date=opening_transaction_date.date(),
        enter_date=opening_transaction_date,
        description="a month ago balance",
        value=balance,
        from_account=opening_balance,
        to_account=acc)

single_transaction(
    post_date=transaction_date.date(),
    enter_date=transaction_date,
    description="yesterday withdrawal from bank to cash",
    value=TRANSACTION_VALUE,
    from_account=bank,
    to_account=cash)
 
mock_book.flush()

mock_book.save()