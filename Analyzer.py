import IOHandler

class Analyzer:

    def __init__(self):
        self.trends = []
        self.assets = []

    def addTrend(self, trend):
        self.trends.append(IOHandler.readGoogleTrendsCSV(trend))
        print(self.trends[0])

    def addAsset(self, asset):
        self.assets.append(IOHandler.readAssetReturnsCSV(asset))
        print(self.assets[0])

    #def correlation(self, trend, asset):


analyzer = Analyzer()
analyzer.addTrend("report")
analyzer.addAsset("^GSPC")