from sklearn.linear_model import LinearRegression
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

from utils import MONTHS

datetime_list_to_ordinal = lambda x: [
    datetime(year=xy, month=xm, day=1).toordinal() for (xy, xm) in x]

def get_linear_regression(x_train, y_train, x_pred):
    x_train = datetime_list_to_ordinal(x_train)
    x_pred = datetime_list_to_ordinal(x_pred)
    x_train = np.asarray(x_train).reshape(-1, 1)
    y_train = np.asarray(y_train).reshape(-1, 1)
    x_pred = np.asarray(x_pred).reshape(-1, 1)

    # Create linear regression object
    reg = LinearRegression()
    # print(stub_x, y_wo_front_and_back)
    reg.fit(x_train, y_train)

    return reg.predict(x_pred).transpose()[0]