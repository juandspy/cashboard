"""Constant values of the program.
"""
from datetime import datetime


now = datetime.now()

METRICS_PER_ROW = 4

SELECTBOX_HOME = "Home"
SELECTBOX_INCOME_EXPENSE = "Income and expenses"
SELECTBOX_CUSTOM_QUERY = "Run a custom query"


SQL_QUERY__CUSTOM_START = """
SELECT 
  SUM(value_num) 
FROM 
  (
    SELECT 
      DISTINCT s1.value_num / 100. AS value_num, 
      t1.description, 
      t1.post_date, 
      a1.name AS from_account, 
      a1.account_type AS from_account_type, 
      a2.name AS to_account, 
      a2.account_type AS to_account_type 
    from 
      splits s1 
      INNER JOIN splits s2 ON s1.tx_guid = s2.tx_guid 
      INNER JOIN transactions t1 ON t1.guid = s2.tx_guid 
      INNER JOIN accounts a1 ON s1.account_guid = a1.guid 
      INNER JOIN accounts a2 ON s2.account_guid = a2.guid 
    where 
      a1.name != a2.name 
      AND a2.account_type == "EXPENSE"
      AND t1.description LIKE "CUSTOM_START%" 
  )
"""
