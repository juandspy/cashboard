import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from testdata.mocks import mock_book
from make_sql import run_sql
from testdata.const import (
    BANK_ACCOUNT_NAME,
    CASH_ACCOUNT_NAME,
    OPENING_BALANCE_NAME,
    ASSETS_NAME,
    BANK_SUB_ACCOUNT_1_NAME,
    BANK_SUB_ACCOUNT_2_NAME,
    EXPENSES_NAME,
    EMPTY_ASSETS_NAME,
    INCOMES_NAME,
)


def test_run_sql():
    results = run_sql(mock_book, "SELECT name FROM accounts")
    accounts = []
    for row in results:
        accounts.append(row[0])
    assert BANK_ACCOUNT_NAME in accounts
    assert CASH_ACCOUNT_NAME in accounts
    assert OPENING_BALANCE_NAME in accounts
    assert ASSETS_NAME in accounts
    assert BANK_SUB_ACCOUNT_1_NAME in accounts
    assert BANK_SUB_ACCOUNT_2_NAME in accounts
    assert EXPENSES_NAME in accounts
    assert EMPTY_ASSETS_NAME in accounts
    assert INCOMES_NAME in accounts
