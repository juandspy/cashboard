from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

from utils import MONTHS

datetime_list_to_ordinal = lambda x: [
    datetime(year=xy, month=xm, day=1).toordinal() for (xy, xm) in x]

def treat_inputs(x_train, y_train, x_pred):
    x_train = datetime_list_to_ordinal(x_train)
    x_pred = datetime_list_to_ordinal(x_pred)
    x_train = np.asarray(x_train).reshape(-1, 1)
    y_train = np.asarray(y_train).reshape(-1, 1)
    x_pred = np.asarray(x_pred).reshape(-1, 1)
    return x_train, y_train, x_pred

def get_linear_regression(x_train, y_train, x_pred):
    x_train, y_train, x_pred = treat_inputs(x_train, y_train, x_pred)
    # Create linear regression object
    reg = LinearRegression()
    # print(stub_x, y_wo_front_and_back)
    reg.fit(x_train, y_train)

    return reg.predict(x_pred).transpose()[0]

def get_polynomial_regression(x_train, y_train, x_pred, degree=2):
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