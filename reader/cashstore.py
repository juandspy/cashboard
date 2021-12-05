import piecash
from typing import List

from reader.accounts import get_book_accounts_of_type


DEFAULT_ASSETS_DEPTH = 0
DEFAULT_EXPENSES_DEPTH = 0

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

        self.set_assets_depth(DEFAULT_ASSETS_DEPTH)
        self.set_expenses_depth(DEFAULT_EXPENSES_DEPTH)

    def set_assets_depth(self, depth):
        """Updates self.assets to the desired depth.
        """
        self.assets = get_book_accounts_of_type("ASSET", self.book, depth)
        self.update_assets_splits()

    def set_expenses_depth(self, depth):
        """Updates self.expenses to the desired depth.
        """
        self.expenses = get_book_accounts_of_type("EXPENSE", self.book, depth)
        self.update_expenses_splits()

    def update_assets_splits(self):
        for asset in self.assets:
            asset.split_df = self.splits_df.loc[self.splits_df["account.fullname"] == asset.account.fullname]

    def update_expenses_splits(self):
        for expense in self.expenses:
            expense.split_df = self.splits_df.loc[self.splits_df["account.fullname"] == expense.account.fullname]