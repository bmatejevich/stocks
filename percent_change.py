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
    with open('tickers.pickle','wb') as f:
        pickle.dump(ticker_list,f)
    return ticker_list

def delete_old_data():
    if path.isdir('stock_dfs') == True:
        shutil.rmtree('stock_dfs')

def get_data_from_yahoo(tickers,start=dt.datetime(2020,7,14),end=dt.datetime(2020,10,14)):
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
    with open("tickers.pickle","rb") as f:
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

def check_percent_change(main_df,stock_list,week_win_percent = 5,month_win_percent = 10,three_month_win_percent = 30,year_win_percent = 100):
    year = 260
    three_months = 66
    month = 22
    week = 5

    weekly_winners = []
    monthly_winners = []
    three_month_winners = []
    yearly_winners = []

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

        weekly_percent_change = ((current_value-week_back_value)/week_back_value)*100
        monthly_percent_change = ((current_value-month_back_value)/month_back_value)*100
        three_month_percent_change = ((current_value-three_months_back_value)/three_months_back_value)*100
        yearly_percent_change = ((current_value-year_back_value)/year_back_value)*100

        if weekly_percent_change >= week_win_percent:
            weekly_winners.append(stock_name)
        if monthly_percent_change >= month_win_percent:
            monthly_winners.append(stock_name)
        if three_month_percent_change >= three_month_win_percent:
            three_month_winners.append(stock_name)
        if yearly_percent_change >= year_win_percent:
            yearly_winners.append(stock_name)

    return(weekly_winners,monthly_winners,three_month_winners,yearly_winners)


def main(ticker_list_file,start,end,delete_old,week_win_percent,month_win_percent,three_month_win_percent,year_win_percent):
    stock_list = get_ticker_list(ticker_list_file)
    ticker_list = stock_list
    print("Got ticker list!")

    tickers = save_tickers(ticker_list)
    print("Saved tickers!")

    if delete_old == True:
        delete_old_data()
        print("Deleted old stock files!")

    get_data_from_yahoo(tickers,start,end)
    print("Got data!")

    main_df = compile_data()
    print("Compliled!")

    weekly_winners,monthly_winners,three_month_winners,yearly_winners = check_percent_change(main_df,stock_list,week_win_percent,month_win_percent,three_month_win_percent,year_win_percent)
    print(weekly_winners)
    print(monthly_winners)
    print(three_month_winners)
    print(yearly_winners)


##########################################################
days_back = 500
ticker_list_file = 'tickerlist.csv'
week_win_percent = 15
month_win_percent = 70
three_month_win_percent = 120
year_win_percent = 500

d = datetime.today()
look_back = dt.timedelta(days=days_back)
end = dt.datetime(d.year,d.month,d.day)
start = end - look_back

delete_old = True

main(ticker_list_file,start,end,delete_old,week_win_percent,month_win_percent,three_month_win_percent,year_win_percent)
