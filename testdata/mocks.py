"""Mocks for the reader package"""

from datetime import datetime
from piecash.core.factories import single_transaction

from testdata.accounts import opening_balance, acc, bank, cash, mock_book
from testdata.balance import set_initial_balance

TRANSACTION_VALUE = 100
BANK_INITIAL_VALUE = 1000
CASH_INITIAL_VALUE = 100
MONTHS_AFTER_INITIAL_OPENING = 6

now = datetime.now()

opening_balance_month = now.month - MONTHS_AFTER_INITIAL_OPENING
if opening_balance_month <= 0:
    opening_balance_month += 12
opening_transaction_date = now.replace(month=opening_balance_month, day=1)


for (acc, balance) in zip([bank, cash], [BANK_INITIAL_VALUE, CASH_INITIAL_VALUE]):
    set_initial_balance(opening_transaction_date, balance, opening_balance, acc)

transaction_date = now.replace(day=now.day - 1)

single_transaction(
    post_date=transaction_date.date(),
    enter_date=transaction_date,
    description="yesterday withdrawal from bank to cash",
    value=TRANSACTION_VALUE,
    from_account=bank,
    to_account=cash,
)

mock_book.flush()

mock_book.save()
