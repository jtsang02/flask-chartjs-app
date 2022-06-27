import pandas as pd
import sqlite3
from sqlite3 import Error

# inputs
bt_inputs = {'tickers': ['LBS=F'],
             'start_date': '2020-01-01',
             'end_date': '2022-01-01'}

# create a sql connection
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    con = None
    try:
        con = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return con

# construct a query for each setting
def read_db(con, setting):
    """ read a database connection to the SQLite database
        specified by the db_file
    :param con: connection object
    :param setting: 
    :returns: date and price as lists
    """
    select_tickers = bt_inputs['tickers']
    start_date = bt_inputs['start_date']
    end_date = bt_inputs['end_date']

    c = con.cursor()

    query = """
    select * from '""" + (setting) + """'
    where ticker in ('""" + "','".join(select_tickers) + """')
    and Date >= '""" + start_date + """'
    and Date < '""" + end_date + "'"
    c.execute(query.replace('\n', ' '))

    #create dataframe in panda
    dataset = pd.DataFrame(c.fetchall(), columns=['Date', 'ticker', setting])
    # convert to datetime
    dates =  pd.to_datetime(dataset['Date']).dt.strftime('%Y-%m-%d').to_list()
    prices = dataset[setting].to_list()

    return dates, prices


# create a database connection
con = create_connection('stockPrices.db')

# extract data as list from db
dates = read_db(con, 'open')[0]
prices_open = read_db(con, 'open')[1]
prices_close = read_db(con, 'close')[1]
prices_high = read_db(con, 'high')[1]
prices_low = read_db(con, 'low')[1]

# print(prices_open)
