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
# print(test)

# get open prices
open = test['Open']
print(open)

# # get open prices
close = test['Close']
# print(close)

# # get high prices
high = test['High']
# print(high)

# # get low prices
low = test['Low']
# print(low)

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

# inputs
select_tickers = bt_inputs['tickers']
start_date = bt_inputs['start_date']
end_date = bt_inputs['end_date']

# construct 4 querys for each table
query1 = """
select * from open
where ticker in ('"""+ "','".join(select_tickers) + """')
and Date >= '"""+ start_date + """'
and Date < '""" + end_date + "'"
c.execute(query1.replace('\n',' '))
result1 = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'open'])
# convert to datetime
result1['Date'] = pd.to_datetime(result1['Date'])
print(result1)

query2 = """
select * from close
where ticker in ('"""+ "','".join(select_tickers) + """')
and Date >= '"""+ start_date + """'
and Date < '""" + end_date + "'"
c.execute(query2.replace('\n',' '))
result2 = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'close'])
# convert to datetime
result2['Date'] = pd.to_datetime(result2['Date'])
print(result2)

query3 = """
select * from high
where ticker in ('"""+ "','".join(select_tickers) + """')
and Date >= '"""+ start_date + """'
and Date < '""" + end_date + "'"
c.execute(query3.replace('\n',' '))
result3 = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'high'])
# convert to datetime
result3['Date'] = pd.to_datetime(result3['Date'])
print(result3)

query4 = """
select * from low
where ticker in ('"""+ "','".join(select_tickers) + """')
and Date >= '"""+ start_date + """'
and Date < '""" + end_date + "'"
c.execute(query4.replace('\n',' '))
result4 = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'low'])
# convert to datetime
result4['Date'] = pd.to_datetime(result4['Date'])
print(result4)

# https://medium.com/cassandra-cryptoassets/download-and-store-stock-prices-using-python-and-sqlite-e5fa0ea372cc