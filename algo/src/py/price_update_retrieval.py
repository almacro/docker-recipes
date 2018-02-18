#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

# fetch compact price history and save to CSV file

from __future__ import print_function
from datetime import datetime

import warnings
import time

import MySQLdb as mdb
import requests

import sys

# Obtain a database connection to the MySQL instance
db_host = 'sqldb'
db_name = 'securities_master'
con = mdb.connect(
    host=db_host,
    db=db_name,
    read_default_file="~/.my.cnf",
    read_default_group="mysql"
)

apikeyfile = ".apikey"
with open(apikeyfile,"r") as f:
    apikey = f.read()
apikey = apikey.rstrip()

def obtain_list_of_db_tickers():
    """
    Obtains a list of the ticker symbols in the database
    """
    with con:
        cur = con.cursor()
        cur.execute("SELECT id, ticker FROM symbol")
        data = cur.fetchall()
    return [(d[0], d[1]) for d in data]

def get_daily_historic_data_alphav(ticker):
    """
    Obtains data from Alpha Vantage and returns a list of tuples

    ticker: Market ticker symbol, e.g. "GOOG" for Alphabet, Inc.
    """
    # Construct the Alpha Vantage URL with the correct integer query parameters
    outputsize = 'compact'
    datatype = 'csv'

    ticker_tup = (
        ticker, outputsize, datatype, apikey
    )
    alphav_url =  "https://www.alphavantage.co/query"
    alphav_url += "?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s"
    alphav_url += "&outputsize=%s&datatype=%s&apikey=%s"
    alphav_url = alphav_url % ticker_tup
    print(alphav_url)
    
    # Try connecting to Alpha Vantage and obtaining the data
    # On failure, print an error message.
    try:
        av_text = requests.get(alphav_url).text
        # write to file
        csvfile = "%s_%s.csv" % (ticker,outputsize)
        with open(csvfile,"w") as f:
            f.write(av_text)

        av_data = av_text.split("\n")[1:-1]
        prices = []
        for a in av_data:
            p  = a.strip().split(',')
            dt = p[0] # date
            o  = p[1] # open
            h  = p[2] # high
            l  = p[3] # low
            c  = p[4] # close
            ac = p[6] # adjusted close
            vo = p[5] # volume
            d  = p[7] # dividend
            s  = p[8] # split
            prices.append(
                (datetime.strptime(dt, '%Y-%m-%d'),
                 o, h, l, c, ac, vo)
            )
    except Exception as e:
        print("Could not download Alpha Vantage data: %s" % e)
    return prices
    
if __name__ == "__main__":
    # This ignores the warnings regarding Data Truncation
    # from the vendor precision to Decimal(19,4) datatype
    warnings.filterwarnings('ignore')

    start_ticker = 0
    if len(sys.argv) > 1:
        start_ticker = int(sys.argv[1])
        
    # Loop over the tickers and insert the daily historical
    # data into the database
    tickers = obtain_list_of_db_tickers()
    lentickers = len(tickers)
    for i,t in enumerate(tickers):
        if i < start_ticker:
            continue
        
        print(
            "Adding data for %s: %s out of %s" %
            (t[1], i+1, lentickers)
        )
        av_data = get_daily_historic_data_alphav(t[1])
        # take pause to avoid rate limiting on API calls
        time.sleep(10)
    print("Successfully added Alpha Vantage pricing data to DB.")
