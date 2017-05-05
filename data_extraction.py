import datetime as dt
import os
import time
import matplotlib.pyplot as plt
import tqdm as tqdm
import numpy as np
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import bs4 as bs
import pickle
import requests
import pandas_datareader.data as web
from matplotlib import style

style.use('ggplot')

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')        # Make request page from Wikipedia
    soup = bs.BeautifulSoup(resp.text, "html.parser")       # Parse page with BeautifulSoup object
    table = soup.find('table', {'class':'wikitable sortable'})      # Locate table on page
    tickers = []  # Make empty tickers list
    for row in table.findAll('tr')[1:]:     # Iterate through table row from index 1 and on
        ticker = row.findAll('td')[0].text  #
        tickers.append(ticker)      # Append to ticker
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers
# save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2017,12,31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker.replace('.', '-'), 'yahoo', start, end)
                time.sleep(0.5)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except:
                print("DataReader Error")
        else:
            print('Already have {}.csv'.format(ticker))
# get_data_from_yahoo()