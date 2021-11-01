import piecash
from typing import List
import pandas as pd

class Asset:
    """
    Asset is initialized with the asset name, current balance, a dataframe with its transactions, the currency
    it uses and the piecash.Account object.
    """
    def __init__(self, name, current_balance, currency, account=None):
        self.name = name 
        self.current_balance = current_balance 
        self.currency = currency
        self.account = account
        self.split_df = pd.DataFrame()

    def set_split_df(self, split_df):
        self.split_df = split_df
    
    def set_delta(self, delta):
        self.delta = delta
    
    def get_daily_balance(self):
        from reader.analisis import get_daily_balance
        return get_daily_balance(self)
    

def get_book_assets(book: piecash.core.book.Book, depth: int = 0) -> List[Asset]:
    """
    Returns all assets from the book with no children. If it finds an account with 
    children but $depth is the desired, it returns that account instead of its
    children.

    Check assets_test.py test_get_book_assets for further understanding.
    """
    assets = []
    for acc in book.accounts(type="ASSET").children:
        assets.extend(get_asset_children(acc, depth=depth))
    return assets

def get_asset_children(acc: piecash.core.account.Account, 
                    current_depth: int = 0, 
                    depth: int = 0) -> List[Asset]:
    """
    Process account children in a loop and return the list of the assets that has no children.
    The assets with children are ignored.
    You can define a depth in order not to go too deep getting the children.

    Check assets_test.py test_get_asset_children for further understanding.
    """   
    if depth == 0:
        return []
    
    assets = []
    for asset in acc.children:
        if current_depth > depth:
            return assets 
        if len(asset.children) <= 1 or current_depth + 1 == depth:
            assets.append(
                Asset(
                    name=asset.name, 
                    current_balance=float(asset.get_balance(natural_sign=False)), 
                    currency=asset.commodity,
                    account=asset)
                )
        else: 
            current_depth += 1 
            sub_assets = get_asset_children(asset, current_depth=current_depth, depth=depth)
            assets.extend(sub_assets)
    return assets