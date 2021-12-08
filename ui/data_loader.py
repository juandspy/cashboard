"""
This module contains the required functions to load the data.
"""
from sqlite3 import Connection
from config.config_parser import parse_config
from reader.cashstore import CashStore

from streamlit import cache as st_cache

config = parse_config("config.toml")

SHOW_MODE = False

# TODO: Find the way to cache this


def load_data(depth: int = 1):
    """
    Loads the data from a GNUCash file.
    """
    store = CashStore(book_path=config.database)
    if SHOW_MODE:
        from testdata.cashbook_generator import mock_book
        store = CashStore(book=mock_book)
    store.set_assets_depth(depth=depth)
    store.set_expenses_depth(depth=depth)
    store.set_incomes_depth(depth=depth)

    return store.assets, store.expenses, store.incomes
