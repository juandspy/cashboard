from reader.accounts import CashAccount
from datetime import datetime


def get_account_delta(account: CashAccount, from_date: datetime.date) -> float:
    """Returns the difference between an account `from_date` balance and now.

    Args:
        asset (reader.accounts.CashAccount): the account.
        from_date (datetime.date): the date from which the delta is calculated.

    Returns:
        [type]: [description]
    """
    df_from_date = account.split_df[
        account.split_df["transaction.post_date"] >= from_date
    ]
    return df_from_date["value"].sum()


def get_account_balance_at_date(
    account: CashAccount, from_date: datetime.date
) -> float:
    df_until_date = account.split_df[
        account.split_df["transaction.post_date"] <= from_date
    ]
    return df_until_date["value"].sum()
