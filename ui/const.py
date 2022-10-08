"""Constant values of the program.
"""
from datetime import datetime


now = datetime.now()

METRICS_PER_ROW = 4

SELECTBOX_HOME = "Home"
SELECTBOX_INCOME_EXPENSE = "Income and expenses"
SELECTBOX_CUSTOM_QUERY = "Run a custom query"


SQL_QUERY__CUSTOM_START = """
SELECT SUM(value_num)/100 FROM (

SELECT joined.value_num, t.description, t.post_date, t.enter_date
FROM
    (
        SELECT to_accounts.tx_guid, from_accounts.account_guid AS from_account, to_accounts.account_guid AS to_account, to_accounts.value_num
        FROM
        (
        SELECT tx_guid, account_guid, value_num
        FROM splits
        WHERE value_num > 0
        ) AS to_accounts,
        (
        SELECT tx_guid, account_guid, value_num
        FROM splits
        WHERE value_num < 0
        ) AS from_accounts
        WHERE to_accounts.tx_guid = from_accounts.tx_guid
    ) AS joined, transactions as t
    WHERE t.guid = joined.tx_guid AND t.description LIKE "CUSTOM_START%"
)
"""
