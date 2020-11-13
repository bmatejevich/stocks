import pickle
import datetime as dt
from datetime import datetime
import os
import os.path
from os import path
import pandas as pd
import pandas_datareader.data as web
from matplotlib import style
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
    with open('../temp/tickers.pickle', 'wb') as f:
        pickle.dump(ticker_list,f)
    return ticker_list

def delete_old_data():
    if path.isdir('../stock_dfs') == True:
        shutil.rmtree('../stock_dfs')

def get_data_from_yahoo(tickers,start=dt.datetime(2018,1,1),end=dt.datetime(2020,10,14)):
    if not os.path.exists('../stock_dfs'):
        os.makedirs('../stock_dfs')
    print(start)
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
    with open("../temp/tickers.pickle", "rb") as f:
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
    return main_df

def get_percent_change(main_df,stock_list):
    year = 260
    three_months = 66
    month = 22
    week = 5

    weekly_winners = {"a":-999}
    monthly_winners = {"a":-999}
    three_month_winners = {"a":-999}
    yearly_winners = {"a":-999}

    year_back_value = 0.0

    for stock_name in stock_list:
        arr = main_df[stock_name]
        arr = arr.to_numpy()

        length = len(arr)
        current_value = arr[length-1]
        week_back_value = arr[length-week-1]
        month_back_value = arr[length-month-1]
        three_months_back_value = arr[length-three_months-1]
        if len(arr)>year:
            year_back_value = arr[length-year-1]

        weekly_percent_change = round(((current_value-week_back_value)/week_back_value)*100,2)
        monthly_percent_change = round(((current_value-month_back_value)/month_back_value)*100,2)
        three_month_percent_change = round(((current_value-three_months_back_value)/three_months_back_value)*100,2)
        yearly_percent_change = round(((current_value-year_back_value)/year_back_value)*100,2)

        stock = str(stock_name)
        weekly_winners[stock] = weekly_percent_change
        monthly_winners[stock] = monthly_percent_change
        three_month_winners[stock] = three_month_percent_change
        yearly_winners[stock] = yearly_percent_change

    weekly_winners = sorted(weekly_winners.items(), key=lambda x: x[1], reverse=True)
    monthly_winners = sorted(monthly_winners.items(), key=lambda x: x[1], reverse=True)
    three_month_winners = sorted(three_month_winners.items(), key=lambda x: x[1], reverse=True)
    yearly_winners = sorted(yearly_winners.items(), key=lambda x: x[1], reverse=True)

    return(weekly_winners,monthly_winners,three_month_winners,yearly_winners)


def main(ticker_list_file,days_back,top_n = 5, delete_old = False):
    d = datetime.today()
    look_back = dt.timedelta(days=days_back)
    end = dt.datetime(d.year, d.month, d.day)
    start = end - look_back
    stock_list = get_ticker_list(ticker_list_file)
    ticker_list = stock_list
    print("Got ticker list!")

    tickers = save_tickers(ticker_list)
    print("Saved tickers!")

    if delete_old == True:
        delete_old_data()
        print("Deleted old stock files!")

    print("Downloading data...")
    get_data_from_yahoo(tickers,start,end)
    print("Got data!")

    main_df = compile_data()
    print("Compliled!")
    print()
    print("-----------------------------------------------------------------------------------------------------------------")

    weekly_winners,monthly_winners,three_month_winners,yearly_winners = get_percent_change(main_df,stock_list)
    print("Top " + str(top_n) + " Weekly Movers: " + str(weekly_winners[0:top_n]))
    print("Top " + str(top_n) + " Monthly Movers: " + str(monthly_winners[0:top_n]))
    print("Top " + str(top_n) + " Three Month Movers: " + str(three_month_winners[0:top_n]))
    print("Top " + str(top_n) + " Yearly Movers: " + str(yearly_winners[0:top_n]))

    print("-----------------------------------------------------------------------------------------------------------------")


main(ticker_list_file ='../stock_lists/cold.csv', days_back = 500, top_n = 4, delete_old = True)
