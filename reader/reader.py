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

class Asset:
    def __init__(self, name, balance, last_month_balance, currency, account=None):
        self.name = name 
        self.balance = balance 
        self.last_mont_balance = last_month_balance
        self.currency = currency
        self.account = account
    
    def set_delta(self, days):
        self.delta = get_asset_delta(self.account, days)
    
    def get_monthly_data(self):
        now = datetime.now()
        data = []
        for i in range(1, 13):
            month = now.month - i
            if month <= 0: month+=12
            month_balance = get_asset_date_balance(self.account, now.replace(month=month))
            data.append(month_balance)
        print(data)
        return data

def get_accounts(book: piecash.core.book.Book) -> List[piecash.core.account.Account]:
    accounts = []
    for acc in book.root_account.children:        
        accounts.append(acc)
    return accounts

def get_assets(book: piecash.core.book.Book) -> List[Asset]:
    """
    Returns all assets with no children.
    """
    assets = []
    for acc in book.accounts(type="ASSET").children:
        assets.extend(process_account(acc))
    return assets

def process_account(acc: piecash.core.account.Account) -> List[Asset]:
    """
    Process account children in a loop and return the list of the assets that has no children.
    """    
    assets = []
    for asset in acc.children:
        if len(asset.children) == 0:
            assets.append(
                Asset(
                    name=asset.name, 
                    balance=asset.get_balance(natural_sign=False), 
                    last_month_balance=0,
                    currency=asset.commodity,
                    account=asset)
                )
        else: 
            process_child(acc)
    return assets

def get_asset_delta(asset: piecash.core.account.Account, date: datetime.time) -> float:
    delta = 0

    for split in asset.splits:
        if split.transaction.enter_date >= date.replace(tzinfo=pytz.utc):
            delta += split.quantity
    return float(delta)

def get_asset_date_balance(asset: piecash.core.account.Account, date: datetime.time) -> float:
    delta = get_asset_delta(asset, date)
    return float(asset.get_balance()) - delta