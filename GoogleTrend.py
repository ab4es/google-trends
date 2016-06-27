class GoogleTrend:

    def __init__(self, trend, df):
        self.trend = trend
        self.df = df

    def __str__(self):
        return "TREND = \'" + self.trend \
               + "\'\n=============================================\n" \
               + str(self.df)