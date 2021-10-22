import piecash
from typing import List
from datetime import datetime
import pytz


class CashStore:
    def __init__(self, book_path=None, book=None):
        if ( book == None ) & ( book_path != None ): 
            self.book =  piecash.open_book(
                book_path, 
                readonly=True, 
                do_backup=False)
        elif book != None:
            self.book = book
        else:
            raise ValueError("Need book_path or book")
        
        self.accounts = get_accounts(self.book)

class asset:
    def __init__(self, name, balance, last_month_balance, account=None):
        self.name = name 
        self.balance = balance 
        self.last_mont_balance = last_month_balance

        self.account = account

def get_accounts(book: piecash.core.book.Book) -> List[asset]:
    accounts = []
    for acc in book.root_account.children:        
        accounts.append(acc)
    return accounts

def get_assets(book: piecash.core.book.Book) -> List[asset]:
    assets = []
    for acc in book.accounts(type="ASSET").children:
        assets.append(
            asset(
                name=acc.name, 
                balance=acc.get_balance(natural_sign=False), 
                last_month_balance=0,
                account=acc)
        )
    return assets

def get_asset_delta(book: piecash.core.book.Book, asset: piecash.core.account.Account, days: int) -> float:
    delta = 0
    now = datetime.now().replace(tzinfo=pytz.utc)

    for split in asset.splits:
        if split.transaction.enter_date > now.replace(day=days):
            delta += split.quantity
    return delta