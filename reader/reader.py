import piecash
from typing import List
from datetime import datetime, timedelta
import pytz


class CashStore:
    def __init__(self, book_path=None, book=None):
        if ( book == None ) & ( book_path != None ): 
            self.book =  piecash.open_book(
                book_path, 
                readonly=True, 
                do_backup=False,
                open_if_lock=True)
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
        data = [0 for i in range(12)]
        for i in range(1, now.month + 1):
            next_month_first_day = datetime(year=now.year, month=i+1, day=1)
            month_last_day = next_month_first_day - timedelta(days=1)
            month_balance = get_asset_date_balance(self.account, month_last_day) # calculate balance for first day of month
            data[i-1] = month_balance
        return data

def get_accounts(book: piecash.core.book.Book) -> List[piecash.core.account.Account]:
    accounts = []
    for acc in book.root_account.children:        
        accounts.append(acc)
    return accounts

def get_assets(book: piecash.core.book.Book, depth: int = 0) -> List[Asset]:
    """
    Returns all assets with no children.
    """
    assets = []
    for acc in book.accounts(type="ASSET").children:
        assets.extend(process_account(acc, depth=depth))
    return assets

def process_account(acc: piecash.core.account.Account, 
                    actual_depth: int = 0, 
                    depth: int = 0) -> List[Asset]:
    """
    Process account children in a loop and return the list of the assets that has no children.
    """    
    assets = []
    for asset in acc.children:
        print("asset", asset.name, "actual depth", actual_depth, "depth", 0, "chilndre", len(asset.children))
        if len(asset.children) <= 1 or actual_depth + 1 == depth:
            assets.append(
                Asset(
                    name=asset.name, 
                    balance=asset.get_balance(natural_sign=False), 
                    last_month_balance=0,
                    currency=asset.commodity,
                    account=asset)
                )
        else: 
            actual_depth += 1 
            sub_assets = process_account(asset, actual_depth=actual_depth, depth=depth)
            assets.extend(sub_assets)
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