

# Volatility.py

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *


class Volatility(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        self.symbol = self.AddEquity("SPY", Resolution.Minute).Symbol
        self.atr = self.ATR(self.symbol, 14)

        self.SetWarmUp(14)

    def OnData(self, data):

        if not (self.atr.IsReady):
            return

        holdings = self.Portfolio[self.symbol].Quantity
        price = data[self.symbol].Close

        if holdings == 0:
            if price > (self.atr.Current.Value * 2) + price:
                self.MarketOrder(self.symbol, int(self.Portfolio.Cash / price))
        elif holdings > 0:
            if price < (price - (self.atr.Current.Value * 2)):
                self.MarketOrder(self.symbol, -holdings) 
            elif price < (price - (self.atr.Current.Value * .5)):
                self.MarketOrder(self.symbol, -holdings)
                
                # trailing stop loss 
                stop_price = price - (self.atr.Current.Value * .5)
                self.stopMarketTicket = self.StopMarketOrder(self.symbol, -holdings, stop_price)