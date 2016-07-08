import IOHandler
import matplotlib.pyplot as plt
import pandas as pd

class Analyzer:

    def __init__(self):
        self.trends = []
        self.assets = []

    def addTrend(self, trend):
        self.trends.append(IOHandler.readGoogleTrendsCSV(trend))
        #print(self.trends[0])
        print('Added Trend ', '\'', trend, '\'\n', sep='')

    def addAsset(self, asset):
        self.assets.append(IOHandler.readAssetReturnsCSV(asset))
        #print(self.assets[0])
        print('Added Asset ', '\'', asset, '\'\n', sep='')

    #def correlation(self, trend, asset):

    def plotAsset(self, asset):
        rolling = asset.df['std_return'].rolling(center=False,window=12).mean()
        pd.tools.plotting.autocorrelation_plot(asset.df['std_return'])
        #rolling.plot(color='red')
        plt.show()




analyzer = Analyzer()
analyzer.addTrend("report")
analyzer.addAsset("^GSPC")
analyzer.plotAsset(analyzer.assets[0])