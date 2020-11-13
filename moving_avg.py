import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader.data as web
import matplotlib.dates as mdates
from datetime import datetime


style.use('ggplot')

def main(start,end,stock,window_size):
    df = web.DataReader(stock, 'yahoo', start, end)
    window_string = str(window_size)+'ma'
    volume_string = str(window_size)+'D'

    df[window_string] = df['Adj Close'].rolling(window=window_size).mean()
    df.dropna(inplace=True)
    df_volume = df['Volume'].resample(volume_string).sum()

    ax1 = plt.subplot2grid((6,1),(0,0),rowspan=4,colspan=1)
    ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)
    ax1.xaxis_date()
    ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)

    ax1.plot(df.index,df['Adj Close'])
    ax1.plot(df.index,df[window_string])
    ax2.bar(df.index,df['Volume'])

    title = str(window_size) + " day moving average"
    plt.suptitle(title)
    plt.xlabel('Date')

    plt.show()


d = datetime.today()
start = dt.datetime(2000,1,1)
end = dt.datetime(d.year,d.month,d.day)

main(start,end,stock = 'NIO',window_size=20)