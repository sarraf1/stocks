import pandas as pd
import os
#import quandl
import time
from datetime import datetime

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")
import re

import csv
import pandas_datareader.data as pdr

#import urllib2
#from urllib2 import urlopen
from urllib.request import urlopen

auth_tok = open("auth.txt","r").read().rstrip()
path = os.getcwd()
intrapath = path + '/intraQuarter'

startdate = "2000-1-1"
enddate = "2017-10-10"

#data = quandl.get("WIKI/KO", trim_start="2000-12-12", trim_end = "2014-12-30", auth_token=auth_tok)

#print(data["Adj. Close"])

def Stock_Prices():
    df = pd.DataFrame()
    statspath = path+"/_KeyStats"
    stock_list = [x[0] for x in os.walk(statspath)]

    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split("/")[-1]
            print(ticker)
            name = "WIKI/"+ticker.upper()
            data = quandl.get(name, 
                    trim_start="2000-12-12", 
                    trim_end = "2014-12-30", 
                    auth_token=auth_tok)
            print("Success")
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis=1)
        except Exception as e:
            print(str(e))
    print("End of loop")
    df.to_csv("stock_prices.csv")

def GetDividends():
    ##file
    return 0

def getsp500():
    file=open('s-and-p-500-companies/data/constituents.csv','r')
    g=csv.reader(file)
    mylist=[]

    next(g)
    for row in g:
        mylist.append(row[0])
##    g.close()
    return mylist

def getdividend(ticker, start, end):
    data_source = 'yahoo'
    return pdr.DataReader(ticker, 'yahoo-dividends', start, end)

def Key_Stats(gather="PE Ratio", type=1):
    statspath = intrapath + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    stock_list = sorted(stock_list) #Read stock folders alphabetically
    ticker_list = []

    df=pd.DataFrame(columns= ['Ticker','PE Ratio'])
    #print(stock_list[0], stock_list[1])
    #time.sleep(5)
    #print('\n$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

    for each_dir in stock_list[1:559]:
        #print(each_dir)
        ticker=each_dir.split(statspath + '/')[1]
        ticker_list.append(ticker)
        print(ticker)

        try:
            yahooSrc = 'http://finance.yahoo.com/quote/AAPL'
            sourceCode = urlopen('http://finance.yahoo.com/q/ks?s='+ticker).read().decode('utf-8')
            peRatio = sourceCode.split('\"trailingPE\":{\"raw\":')[1].split(',\"fmt\"')[0]
        except Exception as e:
            print('PERATIO ERROR: {0}'.format(e))


        df=df.append({'Ticker':ticker,
                      'PE Ratio':peRatio,
                      },
                      ignore_index=True)

        #time.sleep(1)
    # Plot the differences

    save=gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)


def FixCSV(myfile='PERatio.csv'):
    with open(myfile) as csvfile:
        #with open('output.csv', )
        for i in csvfile:
            print(i)
        

def Stock_Prices():

    newlist=getsp500()
    for i in newlist:
        print(i)

    test=getdividend('QCOM',startdate,enddate)
    print(test)

Key_Stats()
#FixCSV()

