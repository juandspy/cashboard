"""Helper functions to generate the expenses Piechart.
"""
from typing import List
import unicodedata
import plotly.graph_objects as go

from reader.accounts import CashAccount

# TODO: Make a plot_sunburst using the parents.


def plot_pie(labels: List[str], values: List[float]) -> go.Figure:
    """Plots a pie graph.

    Args:
        labels (List[str]): labels.
        values (List[float]): values.

    Returns:
        plotly.graph_objects.Figure: the pie chart Plotly figure.
    """
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig


def plot_expenses(expenses: List[CashAccount]) -> go.Figure:
    """Plots a piechart of the expenses.

    Args:
        expenses (List[CashAccount]): list of expenses accounts.

    Returns:
        plotly.graph_objects.Figure: the pie chart Plotly figure.
    """
    labels = []
    values = []
    for expense in expenses:
        labels.append(expense.name)
        values.append(expense.current_balance)
    labels = remove_accents(labels)
    labels, values = remove_zeros(labels, values)
    return plot_pie(labels, values)


def remove_zeros(
    labels: List[str], values: List[float]) \
        -> (List[str], List[float]):
    """Remove zeros from the two input lists in case `values` element is 0.

    Args:
        labels (List[str]): first list.
        values (List[float]): the list that can have values set to 0.

    Returns:
        List[str]: first list.
        List[float]: the list that can have values set to 0.
    """
    l_out, v_out = [], []
    for (label, value) in zip(labels, values):
        if value != 0:
            l_out.append(label)
            v_out.append(value)
    return l_out, v_out


def remove_accents(my_list: List[str]) -> List[str]:
    """Remove the accents from a list of strings.

    Args:
        my_list (List[str]): the input list.

    Returns:
        List[str]: the list without accents.
    """
    out = []
    for string in my_list:
        nfkd_form = unicodedata.normalize('NFKD', string)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        out.append(only_ascii.decode())
    return out
