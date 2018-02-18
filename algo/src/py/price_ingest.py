#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_ingest.py

# process downloaded CSV files and save tuples to database

from __future__ import print_function
from datetime import datetime

import warnings
import time

import MySQLdb as mdb
import requests

import os.path
import string

# Obtain a database connection to the MySQL instance
db_host = 'sqldb'
db_name = 'securities_master'
con = mdb.connect(
    host=db_host,
    db=db_name,
    read_default_file="~/.my.cnf",
    read_default_group="mysql"
)

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
    # Construct the data file name with the correct integer query parameters
    csvfile = '%s_full.csv' % ticker
    
    if os.path.exists(csvfile):
        with open(csvfile,"r") as f:
            av_text = f.readlines()
    else:
        print("WARN prices file not found: %s" % csvfile)
        return []

    try:
        av_data = string.join(av_text).split("\n")[1:-1]
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

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
    """
    Takes a list of tuples of daily data and adds it to the
    MySQL database. Appends the vendor ID and symbol ID to the data.

    daily data: List of tuples of the OHLC data (with adj_close and volume)
    """
    # Create the time now
    now = datetime.utcnow()

    # Amend the data to include the vendor ID and symbol ID
    daily_data = [
        (data_vendor_id, symbol_id, d[0], now, now,
         d[1], d[2], d[3], d[4], d[5], d[6])
        for d in daily_data
    ]

    # Create the insert strings
    column_str = """data_vendor_id, symbol_id, price_date, created_date,
                    last_updated_date, open_price, high_price, low_price,
                    close_price, volume, adj_close_price"""
    insert_str = ("%s, " * 11)[:-2]
    final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)

    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    with con:
        cur = con.cursor()
        cur.executemany(final_str, daily_data)

if __name__ == "__main__":
    # This ignores the warnings regarding Data Truncation
    # from the vendor precision to Decimal(19,4) datatype
    warnings.filterwarnings('ignore')

    # Loop over the tickers and insert the daily historical
    # data into the database
    tickers = obtain_list_of_db_tickers()
    lentickers = len(tickers)
    for i,t in enumerate(tickers):
        print(
            "Adding data for %s: %s out of %s" %
            (t[1], i+1, lentickers)
        )
        av_data = get_daily_historic_data_alphav(t[1])
        insert_daily_data_into_db('1', t[0], av_data)
    print("Successfully added Alpha Vantage pricing data to DB.")
