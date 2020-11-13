import pickle
import datetime as dt
from datetime import datetime
import os
import os.path
from os import path
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import csv
import shutil

style.use('ggplot')

def get_ticker_list(ticker_list_file):
    with open(ticker_list_file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        ticker_list = []
        for ticker in data:
            #print(ticker[0])
            ticker[0] = ticker[0].replace('\ufeff', '')
            ticker_list.append(ticker[0])
        return ticker_list

def save_tickers(ticker_list):
    with open('temp/tickers.pickle', 'wb') as f:
        pickle.dump(ticker_list,f)
    return ticker_list

def delete_old_data():
    if path.isdir('stock_dfs') == True:
        shutil.rmtree('stock_dfs')

def get_data_from_yahoo(tickers,start=dt.datetime(2018,1,1),end=dt.datetime(2020,10,14)):
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    for ticker in tickers:
        print(ticker)
        if ticker in ['BRK.B','BF.B']:
            print("pass")
            continue
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker,'yahoo',start,end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

def compile_data():
    with open("temp/tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    main_df = pd.DataFrame()
    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date',inplace=True)

        df.rename(columns = {'Adj Close':ticker},inplace=True)
        df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df,how='outer')
    main_df.to_csv('closes.csv')

def visualize_data():
    df = pd.read_csv('temp/closes.csv')
    df_corr = df.corr()

    data= df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(111)

    heatmap = ax.pcolor(data,cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)

    ax.set_xticks(np.arange(data.shape[0])+0.5,minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)

    plt.tight_layout()
    plt.show()

def main(days_back,ticker_list_file,delete_old):
    d = datetime.today()
    look_back = dt.timedelta(days=days_back)
    end = dt.datetime(d.year, d.month, d.day)
    start = end - look_back

    data = get_ticker_list(ticker_list_file)
    ticker_list = data
    print("Got ticker list!")

    tickers = save_tickers(ticker_list)
    print("Saved tickers!")

    if delete_old == True:
        delete_old_data()
        print("Deleted old stock files!")

    get_data_from_yahoo(tickers,start,end)
    print("Got data!")

    compile_data()
    print("Compliled!")

    visualize_data()



main(days_back = 30, ticker_list_file ='stock_lists/medium.csv', delete_old = True)
