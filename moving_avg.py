import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader.data as web
import matplotlib.dates as mdates

style.use('ggplot')

start = dt.datetime(2000,1,1)
end = dt.datetime(2020,1,1)
df = web.DataReader('TSLA','yahoo',start,end)


'''moving average'''
df['100ma'] = df['Adj Close'].rolling(window=100).mean()
#df['x_days_ma'] = df['Adj Close'].rolling(window=x).mean()

df.dropna(inplace=True)

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)
ax1.xaxis_date()

ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)

ax1.plot(df.index,df['Adj Close'])
ax1.plot(df.index,df['100ma'])
ax2.bar(df.index,df['Volume'])


plt.show()
