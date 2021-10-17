import piecash

class CashStore:
    def __init__(self, book_path):
        self.book =  piecash.open_book(
            book_path, 
            readonly=True, 
            do_backup=False)
        
        self.accounts = get_accounts(self.book)
    
def get_accounts(book: piecash.core.book.Book):
    print(book.root_account)
    accounts = []
    for acc in book.root_account.children:
        accounts.append(acc)
    return accounts