"""Helper functions to make regressions
"""
from datetime import datetime
from typing import List
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

import numpy as np


def datetime_list_to_ordinal(input_list: List[datetime]) -> List:
    """Converts a datetime list to ordinal format.

    Args:
        input_list (List[datetime]): the list containing datetime objects.

    Returns:
        List(int): the list of ordinals.
    """
    return [
        datetime(year=xy, month=xm, day=1).toordinal() for (xy, xm) in input_list]


def treat_inputs(x_train: List[datetime], y_train: List[float], x_pred: List[datetime]) \
        -> (List[datetime], List[datetime], List[datetime]):
    """[summary]

    Args:
        x_train (List[datetime]): train set dates.
        y_train (List[float]): train set y values.
        x_pred (List[datetime]):  pred set dates.

    Returns:
        (List[datetime], List[datetime], List[datetime]): the three lists reshaped.
    """
    x_train = datetime_list_to_ordinal(x_train)
    x_pred = datetime_list_to_ordinal(x_pred)
    x_train = np.asarray(x_train).reshape(-1, 1)
    y_train = np.asarray(y_train).reshape(-1, 1)
    x_pred = np.asarray(x_pred).reshape(-1, 1)
    return x_train, y_train, x_pred


def get_linear_regression(
    x_train: List[datetime], y_train: List[float], x_pred: List[datetime]) \
        -> List:
    """Computes a linear regression.

    Args:
        x_train (List[datetime]): train set dates.
        y_train (List[datetime]): train set y values.
        x_pred (List[datetime]):  pred set dates.

    Returns:
        List[datetime]: predictions.
    """
    x_train, y_train, x_pred = treat_inputs(x_train, y_train, x_pred)
    # Create linear regression object
    reg = LinearRegression()
    # print(stub_x, y_wo_front_and_back)
    reg.fit(x_train, y_train)

    return reg.predict(x_pred).transpose()[0]


def get_polynomial_regression(
        x_train: List[datetime], y_train: List[datetime], x_pred: List[datetime], degree: int = 2):
    """Computes a polynomial regression.

    Args:
        x_train (List[datetime]): train set dates.
        y_train (List[datetime]): train set y values.
        x_pred (List[datetime]):  pred set dates.
        degree (int):             the degree of the regression.

    Returns:
        List[datetime]: predictions.
    """
    x_train, y_train, x_pred = treat_inputs(x_train, y_train, x_pred)
    polynomial_features = PolynomialFeatures(degree=degree, include_bias=False)

    linear_regression = LinearRegression()
    pipeline = Pipeline(
        [
            ("polynomial_features", polynomial_features),
            ("linear_regression", linear_regression),
        ]
    )
    pipeline.fit(x_train, y_train)
    return pipeline.predict(x_pred).transpose()[0]
