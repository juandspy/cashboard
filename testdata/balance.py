"""Helper to set the initial balance of an account"""

from piecash.core.factories import single_transaction


def set_initial_balance(date, value, balance_account, account):
    """Set the initial balance of an account"""

    single_transaction(
        post_date=date.date(),
        enter_date=date,
        description="initial balance",
        value=value,
        from_account=balance_account,
        to_account=account,
    )
