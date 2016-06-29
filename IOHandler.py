import csv
import datetime
import pprint
import GoogleTrend
import Asset
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
import pandas

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
    # df = pandas.concat([df[df.index.weekday == 0], df[df.index.weekday == 4]]) # only keep Mondays and Fridays
    df = df.sort_index() # sort by date

    df_calcs = pandas.DataFrame

    print(df)

    # compute returns only across full trading weeks (Monday -> Friday)
    for index, row in df.iterrows():
         date = pandas.to_datetime(index)
         if date.weekday() == 0: # is Monday
             tues = date + datetime.timedelta(days=1)
             wed = date + datetime.timedelta(days=2)
             thur = date + datetime.timedelta(days=3)
             fri = date + datetime.timedelta(days=4)
             if tues in df.index and wed in df.index and thur in df.index and fri in df.index: # trading occurred on corresponding Friday
                # print(date, '->', fri)
                # print(index, "\n", row)
                # print("\n\n\n")
                df_tmp = pandas.DataFrame(data=row)
                df_calcs.append(df_tmp)

    print(df_calcs)

    #df['Returns'] = df['Adj Close'].pct_change() # calculate returns
    #df['Std Returns'] = (df['Returns'] - df['Returns'].mean()) / df['Returns'].std() # standardize returns

    #ohlc = FF.create_ohlc(df.Open, df.High, df.Low, df.Close, dates = df.Date) # save OHLC data

    #return Asset.Asset(asset, df, ohlc)

    # TO-DO: import daily tick data and calculate weekly returns (Monday - Friday)


###########################################################################
#readGoogleTrendsCSV("report")
readAssetReturnsCSV("^GSPC")
