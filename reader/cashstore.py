import piecash
from typing import List

from reader.assets import get_book_assets


DEFAULT_DEPTH = 0

def get_accounts(book: piecash.core.book.Book) -> List[piecash.core.account.Account]:
    """
    Returns the root accounts of the PieCash book without its children.
    """
    accounts = []
    for acc in book.root_account.children:        
        accounts.append(acc)
    return accounts


class CashStore:
    """
    CashStore is initialized to the path to a GNUCash book in SQLite3 format or with a piecash.Book itself
    """
    
    def __init__(self, book_path=None, book=None):
        if ( book == None ) & ( book_path != None ): 
            self.book =  piecash.open_book(
                book_path, 
                readonly=True, 
                do_backup=True,
                open_if_lock=True)
        elif book != None:
            self.book = book
        else:
            raise ValueError("Need book_path or book")
        
        self.accounts = get_accounts(self.book)
        self.splits_df = self.book.splits_df()

        self.set_assets_depth(DEFAULT_DEPTH)

    def set_assets_depth(self, depth):
        """Updates self.assets to the desired depth.
        """
        self.assets = get_book_assets(self.book, depth)
        self.update_assets_splits()
        # print("Setting depth to {} returns {} assets".format(depth, len(self.assets)))

    def update_assets_splits(self):
        for asset in self.assets:
            # print("Gathering data for asset".format(asset.name))
            asset.split_df = self.splits_df.loc[self.splits_df["account.fullname"] == asset.account.fullname]
            # print("Asset {} updated".format(asset.name))
