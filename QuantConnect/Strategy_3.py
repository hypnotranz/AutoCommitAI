

# Trend following strategy using MACD with signal line cross entry and opposite signal or trailing stop exit
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Orders import *
from QuantConnect.Securities import *


class TrendFollowingMACD(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)
        
        self.symbol = "SPY"
        self.atrPeriod = 14
        self.atrMultiplier = 1
        
        # MACD indicator setup
        self.fastPeriod = 12
        self.slowPeriod = 26
        self.signalPeriod = 9
        
        # Set up indicator for the SPY symbol
        self.spy = self.AddEquity(self.symbol, Resolution.Daily).Symbol
        
        # Add indicators to algorithm using helper methods available in QCAlgorithm base class
        macd = self.MACD(self.spy, self.fastPeriod, self.slowPeriod, self.signalPeriod, MovingAverageType.Exponential)
        
        # Use the MACD signal line as our entry indicator for long positions only (filtering out short signals)
        macdSignalLineCrossOver = CrossAbove(macd.Signal, macd.Fast, 1)
        
        # Use the opposite signal or trailing stop as our exit criteria
        macdSignalLineCrossUnder = CrossUnder(macd.Signal, macd.Fast, 1)
        
        # Set up trailing stop using ATR (Average True Range) to calculate stop distance
        atr = AverageTrueRange(self.atrPeriod)
        
    def OnData(self, data):
            if not (data.ContainsKey(self.spy) and data[self.spy] and data[self.spy].Price):
                return
            
            if not (self.IsWarmingUp):
                price = data[self.spy].Price
                
                if not (self.Portfolio.Invested) and macdSignalLineCrossOver:
                    # Enter long position at market price and set stop loss based on ATR * multiplier from current price
                    stopPrice = price - (self.atrMultiplier * atr.Current.Value)
                    quantity = int(self.Portfolio.Cash / price)
                    orderTicket = self.MarketOrder(self.spy, quantity)
                    orderTicket.StopMarket(stopPrice)

                elif macdSignalLineCrossUnder or (self.Portfolio.Invested and price < (stopPrice + atr.Current.Value)):
                    # Exit long position at market price and cancel any open stop loss orders 
                    orderTicket.StopMarket(stopPrice).Cancel()
                    quantity = int(self.Portfolio[self.spy].Quantity * -1)
                    orderTicket = self.MarketOrder(self.spy, quantity)