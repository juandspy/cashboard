"""Helper functions to plot graphs
"""

import plotly.graph_objects as go
from pandas import DataFrame, Series
from streamlit import plotly_chart as st_plotly_chart

from utils import daily_to_monthly, date_index_to_str, fill_series
from predictions import get_linear_regression, get_polynomial_regression
from reader.accounts import CashAccount


class HistoricalPlot:
    """Contains functions to help the user plot some historical plots.
    """

    def __init__(self, name: str):
        """Initialize the class.

        Args:
            name (str): plot's name.
        """
        self.name = name
        self.fig = go.Figure()
        # total_monthly_balance is used to stack the balance of all
        # accounts and make regression based on it
        self.total_monthly_balance: DataFrame = None

    def add_account_balance(self, account: CashAccount):
        """Add a trace to the plot with the account monthly balance.

        Args:
            account (CashAccount): the account.
        """
        daily_balance = account.get_daily_balance()
        monthly_balance = daily_to_monthly(daily_balance)

        # If the account has no transactions, don't add the trace
        if monthly_balance.empty:
            return

        # Stack the balance to the total_monthly_balance
        if self.total_monthly_balance is None:
            # If total_monthly_balance is empty, copy this balance
            self.total_monthly_balance = monthly_balance.copy()
        else:
            # If total_monthly_balance is not empty, add this balance
            self.total_monthly_balance = self.total_monthly_balance.add(
                monthly_balance, fill_value=0)

        self.fig.add_trace(go.Bar(
            x=date_index_to_str(monthly_balance),
            y=monthly_balance.values,
            name=account.name
        ))

    def add_account_diff(self, account: CashAccount, invert: bool = False):
        """Add a trace to the plot with the account monthly gains and expenses.

        Args:
            account (CashAccount): the account.
            invert (bool, optional): whether to invert the sign of the values. Defaults to false.
        """
        daily_balance = account.get_daily_balance()
        monthly_balance = daily_to_monthly(daily_balance)
        if invert:
            monthly_balance = -monthly_balance

        graph_y = monthly_balance_to_diff(monthly_balance).values
        self.fig.add_trace(go.Bar(
            x=date_index_to_str(monthly_balance),
            y=graph_y,
            name=account.name,
            # marker={'color': y},
        ))

    def add_regression(self, degree: int = 1):
        """Add a trace with a regression of the stacked balance.

        Args:
            degree (int, optional): Regression degree. Defaults to 1.
        """
        total_monthly_balance_no_zeros = self.total_monthly_balance.loc[~(
            self.total_monthly_balance == 0)]

        if degree == 1:
            y_pred = get_linear_regression(
                total_monthly_balance_no_zeros.index,
                total_monthly_balance_no_zeros.values,
                self.total_monthly_balance.index)
        else:
            y_pred = get_polynomial_regression(
                total_monthly_balance_no_zeros.index,
                total_monthly_balance_no_zeros.values,
                self.total_monthly_balance.index,
                degree=degree)
        self.fig.add_trace(go.Scatter(
            x=date_index_to_str(self.total_monthly_balance),
            y=y_pred,
            name="prediction"
        ))

    def plot(self):
        """Plots the graph as a streamlit graph object.
        """
        self.fig.update_layout(
            barmode='relative',
            title=self.name)
        st_plotly_chart(self.fig)


def monthly_balance_to_diff(in_s: Series) -> DataFrame:
    """Generates a dataframe with the gains/expenses respective to previous month.

    Args:
        in_s (Series): input dataframe.

    Returns:
        DataFrame: output dataframe.
    """
    if in_s.empty:
        return in_s
    # Remove trailing zeros
    for index, value in in_s.iloc[::-1].items():
        if value == 0:
            in_s.drop(index, inplace=True)
        else:
            break
    out_s = in_s.diff()
    return fill_series(out_s)
