import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader.data as web
import matplotlib.dates as mdates
from datetime import datetime


style.use('ggplot')

start = dt.datetime(2000,1,1)
d = datetime.today()
end = dt.datetime(d.year,d.month,d.day)
df = web.DataReader('NIO','yahoo',start,end)


'''moving average'''
df['5ma'] = df['Adj Close'].rolling(window=5).mean()
#df['x_days_ma'] = df['Adj Close'].rolling(window=x).mean()

df.dropna(inplace=True)

df_volume = df['Volume'].resample('10D').sum()

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)
ax1.xaxis_date()

ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)

ax1.plot(df.index,df['Adj Close'])
ax1.plot(df.index,df['5ma'])
ax2.bar(df.index,df['Volume'])


plt.show()
