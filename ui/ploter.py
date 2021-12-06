"""Helper functions to plot graphs
"""

import plotly.graph_objects as go
from pandas import DataFrame
from streamlit import plotly_chart as st_plotly_chart

from utils import daily_to_monthly, date_index_to_str
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

    def add_account(self, account: CashAccount):
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
            barmode='stack',
            title=self.name)
        st_plotly_chart(self.fig)
