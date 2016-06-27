class Asset:

    def __init__(self, name, df, ohlc):
        self.name = name
        self.df = df
        self.ohlc = ohlc

    def __str__(self):
        return "ASSET = \'" + self.name \
               + "\'\n=============================================\n" \
               + str(self.df)