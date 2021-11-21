import plotly.graph_objects as go
from typing import List

from reader.accounts import CashAccount


def plot_sunburst(labels: List[str], parents: List[str], values: List[float]):
    data = dict(
        character=labels,
        parent=parents,
        value=values)

    print(data)

    fig =go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    return fig

def plot_expenses(expenses: List[CashAccount]):
    labels = []
    parents = []
    values = []
    for expense in expenses:
        labels.append(expense.name)
        parents.append(expense.parent)
        values.append(expense.current_balance)
    labels, parents = remove_accents(labels), remove_accents(parents)
    labels, parents, values = remove_zeros(labels, parents, values)
    return plot_sunburst(labels, parents, values)

def remove_zeros(labels: List[str], parents: List[str], values: List[float]) -> (List[str], List[str], List[float]):
    l_out, p_out, v_out = [], [], []
    for (label, parent, value) in zip(labels, parents, values):
        if value != 0:
            l_out.append(label)
            p_out.append(parent)
            v_out.append(value)
    return l_out, p_out, v_out

import unicodedata

def remove_accents(my_list: List[str]) -> List[str]:
    out = []
    for string in my_list:
        nfkd_form = unicodedata.normalize('NFKD', string)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        out.append(only_ascii.decode())
    return out

