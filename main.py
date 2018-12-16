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

def Key_Stats(gather="Total Debt/Equity (mrq)", type=1):
    statspath = intrapath + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    stock_list = sorted(stock_list) #Read stock folders alphabetically
    ticker_list = []

    df=pd.DataFrame(columns= ['Date','Unix','Ticker','DE Ratio', 'Price', 'Per. Change', 'SP500Price', 'SP500 Per. Change', 'Difference'])
    #print(stock_list[0], stock_list[1])
    #time.sleep(5)
    #print('\n$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

    for each_dir in stock_list[1:20]:
        #print(each_dir)
        ticker=each_dir.split(statspath + '/')[1]
        ticker_list.append(ticker)
        print(ticker)

        have_starting_stock_value = False
        have_starting_sp500_value = False

        files = os.listdir(each_dir)
        files = sorted(files)
##        print(files)
        if len(files) > 0:
            for each_file in files:
                print(each_file)
                date_stamp = datetime.strptime(each_file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp, unix_time)
                full_path = each_dir + '/' + each_file
                with open(full_path, 'r') as this_file:
                    text=this_file.read()
                    if type==1:
                        try:
                            ## Get Values ##
                            try:
                                de_ratio = float(text.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                            #print(de_ratio)
                            except Exception as e:
                                de_ratio = float(text.split(gather + ':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                                #print(str(e), ticker, file)
                                #time.sleep(1)

                            try:
                                yahooSrc = 'http://finance.yahoo.com/quote/AAPL'
                                sourceCode = urlopen('http://finance.yahoo.com/q/ks?s='+ticker).read().decode('utf-8')
                                peRatio = sourceCode.split('\"trailingPE\":{\"raw\"')[1].split(',\"fmt\"')[0]
                            except Exception as e:
                                print('PERATIO ERROR: {0}'.format(e))


                            try:
                                sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                                #sp500_date = '2015-12-24'
                                row = sp500_df[(sp500_df.index) == sp500_date]
                                sp500_close_price = float(row["Adj Close"])
                            except:
                                print('Bad Date!')
                                sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d') #date - 3 days?
                                #sp500_date = '2015-12-24'
                                row = sp500_df[(sp500_df.index) == sp500_date]
                                sp500_close_price = float(row["Adj Close"])
                                pass

                            stock_price = float(text.split('</small><big><b>')[1].split('</b></big>')[0])

                            if not have_starting_stock_value:
                                starting_stock_price = stock_price
                                have_starting_stock_value = True

                            if not have_starting_sp500_value:
                                starting_sp500_price = sp500_close_price
                                have_starting_sp500_value = True

                            #TODO: Change starting value to be previous value
                            stock_p_change = (stock_price - starting_stock_price)*100/starting_stock_price
                            sp500_p_change = (sp500_close_price - starting_sp500_price)*100/starting_sp500_price

                            difference = stock_p_change - sp500_p_change

                            #print(stock_price)

                            df=df.append({'Date':date_stamp,
                                          'Unix':unix_time,
                                          'Ticker':ticker,
                                          'PE Ratio':peRatio,
                                          'DE Ratio':de_ratio,
                                          'Price':stock_price,
                                          'Per. Change':stock_p_change,
                                          'SP500Price':sp500_close_price,
                                          'SP500 Per. Change':sp500_p_change,
                                          'Difference':difference},
                                          ignore_index=True)
                        except Exception as e:
                            print('Error! ', str(e))
                            pass

        #time.sleep(1)
    # Plot the differences
    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])

            plot_df['Difference'].plot(label=each_ticker)
            plt.legend()

        except:
            pass
    plt.show()
    save=gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)



        

def Stock_Prices():

    newlist=getsp500()
    for i in newlist:
        print(i)

    test=getdividend('QCOM',startdate,enddate)
    print(test)

Key_Stats()

