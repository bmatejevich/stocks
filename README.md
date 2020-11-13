# Stocks

##Dowload and install dependencies
```python
git clone https://github.com/bmatejevich/stocks.git
cd stocks
pip install -r requirements.txt
```


##Big Movers Script
```python
python3 big_movers.py
```
Running this script will give you the top N stocks in terms of % change in the last; week, month, three months & year.
You can change the list of stocks analyzed and value of N in the following lines.
```python
main(ticker_list_file = 'stock_lists/cold.csv',days_back = 500,top_n = 4,delete_old = True)
```


##Percent Change Script
```python
python3 percent_change.py
```
Running this script will give you the stocks that have met or exceeded a set % change goal for; week, month, three months & year.
You can change the % change goals and the list of stock considered in the following lines.
```python
main(ticker_list_file = 'stock_lists/medium.csv',delete_old = True,week_win_percent = 15,month_win_percent = 70,three_month_win_percent = 120,year_win_percent = 500)
```

##Moving Average Script
```python
python3 moving_avg.py
```
Running this script will plot the daily value against the N-day moving average.
You can change the stock and window size in the following lines.
```python
main(start,end,stock = 'NIO',window_size=20)
```


##Correlation Script
```python
python3 correlation.py
```
Running this script will plot the correlation between all stocks in the stock list.
You can change the stock_list and time frame in the following lines.
```python
main(days_back = 30, ticker_list_file = 'stock_lists/medium.csv',delete_old = True)
```


