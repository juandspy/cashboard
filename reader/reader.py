import piecash

class CashStore:
    def __init__(self, book_path):
        self.book =  piecash.open_book(
            book_path, 
            readonly=True, 
            do_backup=False)
        
        self.accounts = get_accounts(self.book)

def get_accounts(book: piecash.core.book.Book):
    accounts = []
    for acc in book.root_account.children:        
        accounts.append(acc)
    return accounts

class asset:
    def __init__(self, name, balance, last_month_balance):
        self.name = name 
        self.balance = balance 
        self.last_mont_balance = last_month_balance

def get_assets(book: piecash.core.book.Book):
    assets = []
    for acc in book.accounts(type="ASSET").children:
        assets.append(
            asset(
                name=acc.name, 
                balance=acc.get_balance(natural_sign=False), 
                last_month_balance=0)
        )
    return assets