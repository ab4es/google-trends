import csv
import datetime
import pprint
import GoogleTrend
import Asset
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
import pandas
import numpy as np

def readGoogleTrendsCSV(trend):
    printer = pprint.PrettyPrinter()

    with open('./data/' + trend + '.csv', 'rt') as file:
        reader = csv.reader(file, delimiter = ',')
        counter = 0 # keep track of how many rows have been read
        df = pandas.DataFrame(columns = ['Start', 'End', 'Value'])

        for row in reader:
            if counter >= 5: # first fives lines are superfluous data
                if not row: break # stop after first empty row
                else:
                    start = datetime.datetime.strptime(row[0].split(' - ')[0], "%Y-%m-%d").date()
                    end = datetime.datetime.strptime(row[0].split(' - ')[1], "%Y-%m-%d").date()
                    if (row[1] != " "): # do not add incomplete rows
                        val = int(row[1])
                        df = df.append(pandas.Series([start, end, val],
                                                     index = ['Start','End', 'Value']),
                                       ignore_index = True) # append row to df
            counter += 1

        df['Std Value'] = (df['Value'] - df['Value'].mean()) / df['Value'].std() # standardize values

        return GoogleTrend.GoogleTrend(trend, df)

def readAssetReturnsCSV(asset):
    df = pandas.read_csv('../../Daily/' + asset + '.csv')
    df['Index'] = pandas.to_datetime(df['Index']) # convert dates to Datetime objects
    df = df.set_index('Index') # set Index
    df = df.sort_index() # sort by date

    # Will store the weekly data
    df_calcs = pandas.DataFrame(columns=['period_ended', 'open', 'high', 'low', 'close', 'volume',
                                         'adj.', 'weekly_return'])

    # compute weekly returns only across full trading weeks (Monday -> Friday)
    for index, row in df.iterrows():
         date = pandas.to_datetime(index)
         if date.weekday() == 4: # is Friday
             thur = date + datetime.timedelta(days=-1)
             wed = date + datetime.timedelta(days=-2)
             tues = date + datetime.timedelta(days=-3)
             mon = date + datetime.timedelta(days=-4)
             # trading occurred on corresponding Friday
             if thur in df.index and wed in df.index and tues in df.index and mon in df.index:
                 period_ended = date
                 open = df.loc[mon]['open']
                 close = row['close']
                 low = min(df.loc[mon]['low'], df.loc[tues]['low'], df.loc[wed]['low'], df.loc[thur]['low'],
                           row['close'])
                 high = max(df.loc[mon]['high'], df.loc[tues]['high'], df.loc[wed]['high'], df.loc[thur]['high'],
                           row['high'])
                 volume = df.loc[mon]['volume'] + df.loc[tues]['volume'] + df.loc[wed]['volume'] + \
                          df.loc[thur]['volume'] + row['volume']
                 adj = row['adj.']
                 weekly_return = (row['adj.'] - df.loc[mon]['adj.']) / df.loc[mon]['adj.']
                 #print(mon, '(', df.loc[mon]['adj.'], ') ->', date, '(', row['adj.'], '):', weekly_return*100, '%')
                 week = pandas.Series([period_ended, open, high, low, close, volume, adj, weekly_return])
                 week = week.rename({0: 'period_ended', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume',
                                     6: 'adj.', 7: 'weekly_return'})
                 df_calcs = df_calcs.append(week, ignore_index=True)
    df_calcs = df_calcs.set_index('period_ended') # set index to period_ended

    print(df_calcs, '\n')

    # standardize weekly returns
    df_calcs['std_return'] = (df_calcs['weekly_return'] - df_calcs['weekly_return'].mean()) / \
                             df_calcs['weekly_return'].std()

    print(df_calcs, '\n')

    # save OHLC data
    ohlc = FF.create_ohlc(df_calcs.open, df_calcs.high, df_calcs.low, df_calcs.close, dates=df_calcs.index)

    return Asset.Asset(asset, df, ohlc)


###########################################################################
# df = pandas.DataFrame(np.random.randn(8, 4), columns=['A','B','C','D'])
# print(df)
# s = df.iloc[3]
# print(s)
# print(df.append(s, ignore_index=True))


#readGoogleTrendsCSV("report")
readAssetReturnsCSV("^GSPC")
