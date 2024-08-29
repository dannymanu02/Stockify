import requests
from dotenv import load_dotenv
import os
import yfinance as yf
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.api as sm

import io
import PIL

class dataAnalytics:
    
    company_name = ""

    def __init__(self, name) -> None:
        self.company_name = name

    def fetch_company_details(self, name):
        yf_comp = yf.Ticker(name)
        
        return yf_comp
    
    def get_historical_data(self, name):
        data = yf.download(name, period="max")

        columns_to_round = ['Open', 'High', 'Low', 'Close', 'Adj Close']
        data[columns_to_round] = data[columns_to_round].round(2)

        return data
    
    def plot_closing_prices(self, data):
        # plt.figure(figsize=(12, 6))
        cpot = io.BytesIO()
        plt.plot(data['Close'], label='Close Price')
        plt.title('Stock Closing Prices Over Time')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()

        plt.savefig(cpot, format='png')
        plt.close()
        cpot.seek(0)
        return cpot

    def plot_volume_traded(self, data):
        # plt.figure(figsize=(12, 6))
        vtot = io.BytesIO()
        plt.plot(data['Volume'], label='Volume')
        plt.title('Stock traded volumes Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()

        plt.savefig(vtot, format='png')
        plt.close()
        vtot.seek(0)
        return vtot

    def plot_intraday_diff(self, data):
        data['intraday_change'] = (data['Close'] - data['Open']).abs()
        data['intraday_change_trend'] = ['positive' if (close - open) > 0 else 'negative' for open, close in zip(data['Open'], data['Close'])]

        # plt.figure(figsize=(12, 6))
        iddot = io.BytesIO()
        plt.plot(data['intraday_change'], label='Close Price')
        plt.title('Stock Intraday Difference Prices Over Time')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        
        plt.savefig(iddot, format='png')
        plt.close()
        iddot.seek(0)
        return iddot

    def plot_intraday_change_trend(self, data):
        positive_trend = data[data['intraday_change_trend'] == 'positive']
        negative_trend = data[data['intraday_change_trend'] == 'negative']

        # plt.figure(figsize=(12, 6))

        plt.plot(positive_trend.index, positive_trend['intraday_change'], 'g^', label='Positive Change')

        plt.plot(negative_trend.index, negative_trend['intraday_change'], 'rv', label='Negative Change')

        idctot = io.BytesIO()
        plt.title('Intraday Change with Trend')
        plt.xlabel('Date')
        plt.ylabel('Intraday Change')
        plt.legend()

        plt.savefig(idctot, format='png')
        plt.close()
        idctot.seek(0)
        return idctot

    def plot_decomposition(self, data):
        decomposition = sm.tsa.seasonal_decompose(data['Close'], model='additive', period=5)

        # plt.figure(figsize=(12, 8))
        dec = io.BytesIO()
        plt.subplot(411)
        plt.plot(data['Close'], label='Original')
        plt.legend(loc='upper left')
        plt.subplot(412)
        plt.plot(decomposition.trend, label='Trend')
        plt.legend(loc='upper left')
        plt.subplot(413)
        plt.plot(decomposition.seasonal, label='Seasonality')
        plt.legend(loc='upper left')
        plt.subplot(414)
        plt.plot(decomposition.resid, label='Residuals')
        plt.legend(loc='upper left')
        plt.tight_layout()
        
        plt.savefig(dec, format='png')
        plt.close()
        dec.seek(0)
        return dec

    def get_crisis_covid_data(self, data):
        covid_start = pd.Timestamp('2020-03-01')
        covid_end = pd.Timestamp('2021-12-31')

        crisis_start = pd.Timestamp('2007-07-01')
        crisis_end = pd.Timestamp('2009-06-30')

        # Filter out COVID-19 and 2008 Financial Crisis periods
        covid_data = data[(data.index >= covid_start) & (data.index <= covid_end)]
        crisis_data = data[(data.index >= crisis_start) & (data.index <= crisis_end)]

        return crisis_data, covid_data


    def plot_rec_analysis(self, crisis_data):
        # plt.figure(figsize=(12, 6))
        crisis_cpot = io.BytesIO()
        plt.plot(crisis_data['Close'], label='Close Price')
        plt.title('Stock Closing Prices During Recession')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()

        plt.savefig(crisis_cpot, format='png')
        plt.close()
        crisis_cpot.seek(0)

        crisis_vtot = io.BytesIO()
        plt.figure(figsize=(12, 6))
        plt.plot(crisis_data['Volume'], label='Volume')
        plt.title('Stock traded volumes During Recession')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()

        plt.savefig(crisis_vtot, format='png')
        plt.close()
        crisis_vtot.seek(0)

        decomposition = sm.tsa.seasonal_decompose(crisis_data['Close'], model='additive', period=5)

        # plt.figure(figsize=(12, 8))
        crisis_dec = io.BytesIO()
        plt.subplot(411)
        plt.plot(crisis_data['Close'], label='Original')
        plt.legend(loc='upper left')
        plt.subplot(412)
        plt.plot(decomposition.trend, label='Trend')
        plt.legend(loc='upper left')
        plt.subplot(413)
        plt.plot(decomposition.seasonal, label='Seasonality')
        plt.legend(loc='upper left')
        plt.subplot(414)
        plt.plot(decomposition.resid, label='Residuals')
        plt.legend(loc='upper left')
        plt.tight_layout()

        plt.savefig(crisis_dec, format='png')
        plt.close()
        crisis_dec.seek(0)

        return crisis_cpot, crisis_vtot, crisis_dec
    
    def plot_covid_analysis(self, covid_data):
        # plt.figure(figsize=(12, 6))
        covid_cpot = io.BytesIO()
        plt.plot(covid_data['Close'], label='Close Price')
        plt.title('Stock Closing Prices During Covid')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()

        plt.savefig(covid_cpot, format='png')
        plt.close()
        covid_cpot.seek(0)

        # plt.figure(figsize=(12, 6))
        covid_vtot = io.BytesIO()
        plt.plot(covid_data['Volume'], label='Volume')
        plt.title('Stock traded volumes During Covid')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()

        plt.savefig(covid_vtot, format='png')
        plt.close()
        covid_vtot.seek(0)

        decomposition = sm.tsa.seasonal_decompose(covid_data['Close'], model='additive', period=5)

        # plt.figure(figsize=(12, 8))
        covid_dec = io.BytesIO()
        plt.subplot(411)
        plt.plot(covid_data['Close'], label='Original')
        plt.legend(loc='upper left')
        plt.subplot(412)
        plt.plot(decomposition.trend, label='Trend')
        plt.legend(loc='upper left')
        plt.subplot(413)
        plt.plot(decomposition.seasonal, label='Seasonality')
        plt.legend(loc='upper left')
        plt.subplot(414)
        plt.plot(decomposition.resid, label='Residuals')
        plt.legend(loc='upper left')
        plt.tight_layout()

        plt.savefig(covid_dec, format='png')
        plt.close()
        covid_dec.seek(0)
        return covid_cpot, covid_vtot, covid_dec

# data = yf.download("MSFT", start="2001-01-01", end="2023-12-31")

# data.to_csv("msft.csv")