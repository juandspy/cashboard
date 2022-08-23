# """Generates a mock cashbook to use in the UI
# """

from datetime import datetime
from piecash.core.factories import single_transaction
import random

from testdata.accounts import (
    opening_balance,
    acc,
    sub_bank_1,
    sub_bank_2,
    cash,
    mock_book,
    gas,
    salary,
)
from testdata.balance import set_initial_balance

BANK_1_INITIAL_VALUE = 5000
BANK_2_INITIAL_VALUE = 1000
CASH_INITIAL_VALUE = 500
SALARY_VALUE = 200


now = datetime.now()
opening_transaction_date = now.replace(month=1)

# Fill the accounts initial values
for (acc, balance) in zip(
    [sub_bank_1, sub_bank_2, cash],
    [BANK_1_INITIAL_VALUE, BANK_2_INITIAL_VALUE, CASH_INITIAL_VALUE],
):
    set_initial_balance(opening_transaction_date, balance, opening_balance, acc)

# Create random expenses for each account every month
for month in range(1, 13):
    transaction_date = now.replace(month=month, day=2)
    for (acc, in_balance) in zip(
        [sub_bank_1, sub_bank_2, cash],
        [BANK_1_INITIAL_VALUE, BANK_2_INITIAL_VALUE, CASH_INITIAL_VALUE],
    ):
        # Some expense
        single_transaction(
            post_date=transaction_date.date(),
            enter_date=transaction_date,
            description="a expense",
            value=random.randint(10, 0.05 * in_balance),
            from_account=acc,
            to_account=gas,
        )
    # Some income
    single_transaction(
        post_date=transaction_date.date(),
        enter_date=transaction_date,
        description="salary transaction",
        value=SALARY_VALUE,
        from_account=salary,
        to_account=acc,
    )

mock_book.flush()

mock_book.save()
