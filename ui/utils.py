import streamlit as st
import time
import numpy as np

N_CHART_POINTS = 12
NOISE_PERCENTAGE = 0.7

class Asset: # TODO: Use reader Asset object
    def __init__(self, name, total, currency, delta):
        self.name = name
        self.total = total
        self.currency = currency
        self.delta = delta

    def get_data(self):
        slope = self.total/N_CHART_POINTS
        rand_noise = np.random.rand(N_CHART_POINTS) * NOISE_PERCENTAGE * self.total
        line = [i * slope for i in range(N_CHART_POINTS)]

        return line + rand_noise

@st.cache
def load_data():  # TODO: Use reader functions
    """
    Just an example on how data will be loaded.
    """
    time.sleep(0.5)
    return [
        Asset("Cash", 1020, "€", "-15%"),
        Asset("Bank account", 3520, "€", "+3%"),
        Asset("Cryptos", 2.3467, "BTC", "+0.32"),
    ]