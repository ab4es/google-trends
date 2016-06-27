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
    print(df)
    df['Date'] = pandas.to_datetime(df['Date']) # convert dates to Datetime objects
    #df = df.sort_values(by = 'Date', ascending = True) # sort by Date to correctly calculate pct_change()
    #df['Returns'] = df['Adj Close'].pct_change() # calculate returns
    #df['Std Returns'] = (df['Returns'] - df['Returns'].mean()) / df['Returns'].std() # standardize returns

    #ohlc = FF.create_ohlc(df.Open, df.High, df.Low, df.Close, dates = df.Date) # save OHLC data

    #return Asset.Asset(asset, df, ohlc)

    # TO-DO: import daily tick data and calculate weekly returns (Monday - Friday)


###########################################################################
#readGoogleTrendsCSV("report")
readAssetReturnsCSV("^GSPC")