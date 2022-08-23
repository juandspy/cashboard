"""Accounts generator for the rest of the files in this package"""

import piecash

from testdata.const import (
    BANK_ACCOUNT_NAME,
    BANK_SUB_ACCOUNT_1_NAME,
    BANK_SUB_ACCOUNT_2_NAME,
    OPENING_BALANCE_NAME,
    ASSETS_NAME,
    CURRENT_ASSETS_NAME,
    EMPTY_ASSETS_NAME,
    CASH_ACCOUNT_NAME,
    EXPENSES_NAME,
    CAR_EXPENSES_NAME,
    GAS_EXPENSES_NAME,
    INCOMES_NAME,
    SALARY_INCOMES_NAME,
)

BANK_INITIAL_VALUE = 1000
CASH_INITIAL_VALUE = 100

mock_book = piecash.create_book(currency="EUR")
EUR = mock_book.commodities.get(mnemonic="EUR")

opening_balance = piecash.Account(
    name=OPENING_BALANCE_NAME,
    type="EQUITY",
    parent=mock_book.root_account,
    commodity=EUR,
)

assets = piecash.Account(
    name=ASSETS_NAME,
    type="ASSET",
    parent=mock_book.root_account,
    commodity=EUR,
    placeholder=True,
)

acc = piecash.Account(
    name=CURRENT_ASSETS_NAME,
    type="ASSET",
    parent=assets,
    commodity=EUR,
    placeholder=True,
)

bank = piecash.Account(
    name=BANK_ACCOUNT_NAME,
    type="BANK",
    parent=acc,
    commodity=EUR,
    commodity_scu=BANK_INITIAL_VALUE,
    description="my bank account",
    code="BANK1",
)

sub_bank_1 = piecash.Account(
    name=BANK_SUB_ACCOUNT_1_NAME,
    type="BANK",
    parent=bank,
    commodity=EUR,
    commodity_scu=BANK_INITIAL_VALUE,
    description="my bank subaccount 1",
    code="BANK1_1",
)

sub_bank_2 = piecash.Account(
    name=BANK_SUB_ACCOUNT_2_NAME,
    type="BANK",
    parent=bank,
    commodity=EUR,
    commodity_scu=0,
    description="my bank subaccount 2",
    code="BANK1_2",
)

cash = piecash.Account(
    name=CASH_ACCOUNT_NAME,
    type="CASH",
    parent=acc,
    commodity=EUR,
    commodity_scu=CASH_INITIAL_VALUE,
    description="my cash in wallet",
    code="CASH1",
)

empty_asset = piecash.Account(
    name=EMPTY_ASSETS_NAME,
    type="ASSET",
    parent=acc,
    commodity=EUR,
    placeholder=True,
)

expenses = piecash.Account(
    name=EXPENSES_NAME,
    type="EXPENSE",
    parent=mock_book.root_account,
    commodity=EUR,
    placeholder=True,
)

car = piecash.Account(
    name=CAR_EXPENSES_NAME,
    type="EXPENSE",
    parent=expenses,
    commodity=EUR,
    description="car expenses",
    code="CAR",
)

gas = piecash.Account(
    name=GAS_EXPENSES_NAME,
    type="EXPENSE",
    parent=car,
    commodity=EUR,
    description="gas expenses",
    code="GAS",
)

incomes = piecash.Account(
    name=INCOMES_NAME,
    type="INCOME",
    parent=mock_book.root_account,
    commodity=EUR,
    placeholder=True,
)

salary = piecash.Account(
    name=SALARY_INCOMES_NAME,
    type="INCOME",
    parent=incomes,
    commodity=EUR,
    description="salary income",
    code="SALARY",
)
