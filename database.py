import pandas as pd
import sqlite3
import yfinance as yf

# backtest inputs
bt_inputs = {'tickers': ['LBS=F', 'BA'],
'start_date': '2020-01-01',
'end_date': '2022-01-01'}

# create a sql connection
con = sqlite3.connect('stockPrices.db')
c = con.cursor()
# create open table
query1 = """CREATE TABLE IF NOT EXISTS open (
Date TEXT NOT NULL,
ticker TEXT NOT NULL,
open REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query1.replace('\n',' '))
# create close table
query2 = """CREATE TABLE IF NOT EXISTS close (
Date TEXT NOT NULL,
ticker TEXT NOT NULL,
close REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query2.replace('\n',' '))
# create high table
query3 = """CREATE TABLE IF NOT EXISTS high (
Date TEXT NOT NULL,
ticker TEXT NOT NULL,
high REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query3.replace('\n',' '))
# create low table
query4 = """CREATE TABLE IF NOT EXISTS low (
Date TEXT NOT NULL,
ticker TEXT NOT NULL,
low REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query4.replace('\n',' '))

def download(bt_inputs, proxy = None):
    data = yf.download(tickers= bt_inputs['tickers'],
                       start = bt_inputs['start_date'],   
                       end = bt_inputs['end_date'],
                       interval = '1d',
                       prepost = True,
                       threads = True,
                       proxy = proxy)
    return data

test = download(bt_inputs)

# get open prices
open = test['Open']

# # get open prices
close = test['Close']

# # get high prices
high = test['High']

# # get low prices
low = test['Low']

# convert wide to long
open_long = pd.melt(open.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name = "ticker", value_name = "open")
close_long = pd.melt(close.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name = "ticker", value_name = "close")
high_long = pd.melt(high.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name = "ticker", value_name = "high")
low_long = pd.melt(low.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name = "ticker", value_name = "low")

# push data into database
open_long.to_sql('open', con, if_exists='replace', index=False)
close_long.to_sql('close', con, if_exists='replace', index=False)
high_long.to_sql('high', con, if_exists='replace', index=False)
low_long.to_sql('low', con, if_exists='replace', index=False)

# pull data from database

# # inputs
# select_tickers = bt_inputs['tickers']
# start_date = bt_inputs['start_date']
# end_date = bt_inputs['end_date']

# # construct 4 querys for each table
# query1 = """
# select * from open
# where ticker in ('"""+ "','".join(select_tickers) + """')
# and Date >= '"""+ start_date + """'
# and Date < '""" + end_date + "'"
# c.execute(query1.replace('\n',' '))
# resultOpen = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'open'])
# # convert to datetime
# resultOpen['Date'] = pd.to_datetime(resultOpen['Date'])
# # print(resultOpen)

# query2 = """
# select * from close
# where ticker in ('"""+ "','".join(select_tickers) + """')
# and Date >= '"""+ start_date + """'
# and Date < '""" + end_date + "'"
# c.execute(query2.replace('\n',' '))
# resultClose = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'close'])
# # convert to datetime
# resultClose['Date'] = pd.to_datetime(resultClose['Date'])
# # print(resultClose)

# query3 = """
# select * from high
# where ticker in ('"""+ "','".join(select_tickers) + """')
# and Date >= '"""+ start_date + """'
# and Date < '""" + end_date + "'"
# c.execute(query3.replace('\n',' '))
# resultHigh = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'high'])
# # convert to datetime
# resultHigh['Date'] = pd.to_datetime(resultHigh['Date'])
# # print(resultHigh)

# query4 = """
# select * from low
# where ticker in ('"""+ "','".join(select_tickers) + """')
# and Date >= '"""+ start_date + """'
# and Date < '""" + end_date + "'"
# c.execute(query4.replace('\n',' '))
# resultLow = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'low'])
# # convert to datetime
# resultLow['Date'] = pd.to_datetime(resultLow['Date'])


# https://medium.com/cassandra-cryptoassets/download-and-store-stock-prices-using-python-and-sqlite-e5fa0ea372cc