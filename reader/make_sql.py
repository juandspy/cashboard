"""This module is intended to run SQL queries agains the database."""

import piecash
from sqlalchemy.engine.result import ResultProxy


def run_sql(book: piecash.core.book.Book, query: str) -> ResultProxy:
    """
    Run a SQL query on a piecash book.

    There is no limitations in the query scope, so be careful with this function.
    """
    results = book.session.execute(query)
    return results
