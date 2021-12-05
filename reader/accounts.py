import piecash
from typing import List
import pandas as pd

class CashAccount:
    """
    CashAccount is initialized with the account name, current balance, a dataframe with its transactions, the currency
    it uses and the piecash.Account object.
    """
    def __init__(self, name, current_balance, currency, account=None, parent=''):
        self.name = name 
        self.current_balance = current_balance 
        self.currency = currency
        self.account = account
        self.split_df = pd.DataFrame()
        self.parent = parent

    def set_split_df(self, split_df):
        self.split_df = split_df
    
    def set_delta(self, delta):
        self.delta = delta
    
    def get_daily_balance(self):
        from reader.analisis import get_daily_balance
        return get_daily_balance(self)
    

def get_account_children(acc: piecash.core.account.Account, 
                    current_depth: int = 0, 
                    depth: int = 0) -> List[CashAccount]:
    """
    Process account children in a loop and return the list of the accounts that has no children.
    The accounts with children are ignored.
    You can define a depth in order not to go too deep getting the children.

    Check accounts_test.py test_get_account_children for further understanding.
    """   
    if depth == 0:
        return []
    
    accounts = []
    for account in acc.children:
        if current_depth > depth:
            return accounts 
        if len(account.children) < 1 or current_depth + 1 == depth:
            new_account = (
                CashAccount(
                    name=account.name, 
                    current_balance=float(account.get_balance(natural_sign=False)), 
                    currency=account.commodity,
                    account=account,
                    parent=acc.name)
                )
            accounts.append(new_account)
        else: 
            current_depth += 1 
            sub_accounts = get_account_children(account, current_depth=current_depth, depth=depth)
            accounts.extend(sub_accounts)
    return accounts


def get_book_accounts_of_type(type: str, book: piecash.core.book.Book, depth: int = 0) -> List[CashAccount]:
    """
    Returns all assets from the book with no children. If it finds an account with 
    children but $depth is the desired, it returns that account instead of its
    children.

    Check assets_test.py test_get_book_assets for further understanding.
    """
    account_of_type = book.accounts(type=type)
    return get_account_children(account_of_type, depth=depth)