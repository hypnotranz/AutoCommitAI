

# Trend Following Strategy with Moving Average Ribbon Indicator, Price Crossing Ribbon Entry, Opposite Signal or Trailing Stop Exit, and 1x ATR Stop Criteria

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import ExponentialMovingAverage, IndicatorExtensions
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Orders import OrderDirection, StopMarketOrder


class TrendFollowingMovingAverageRibbon(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2020, 6, 1)
        self.SetCash(100000)

        self.symbol = "SPY"

        # Create a list of exponential moving averages for the ribbon
        self.emas = [ExponentialMovingAverage(30), ExponentialMovingAverage(60), ExponentialMovingAverage(90),
                     ExponentialMovingAverage(120), ExponentialMovingAverage(150), ExponentialMovingAverage(180)]

        for ema in self.emas:
            self.AddIndicator(self.symbol, ema)

    def OnData(self, data: TradeBar):
        # Wait for all EMAs to be ready
        if not all(map(lambda x: x.IsReady, self.emas)):
            return

        # Calculate the ribbon value as the average of all EMAs
        ribbon = sum(map(lambda x: x.Current.Value, self.emas)) / len(self.emas)

        # Buy if price crosses above the ribbon
        if data.Close > ribbon and not self.Portfolio.Invested:
            stop_price = data.Close - (self.ATR(self.symbol).Current.Value * 1)
            self.StopMarketOrder(self.symbol, -self.Portfolio.Cash / data.Close,
                                  stop_price).Tag = "Exit Long"

            self.MarketOrder(self.symbol, int(self.Portfolio.Cash / data.Close)).Tag = "Enter Long"

        # Sell if price crosses below the ribbon or stop order is triggered
        elif (data.Close < ribbon and self.Portfolio.Invested) or any(
                [x.IsActive and x.Tag == "Exit Long" for x in self.Transactions.GetOpenOrders()]):
            stop_price = max([x.StopPrice for x in self.Transactions.GetOpenOrders() if x.Tag == "Exit Long"])
            exit_price = max([data.Close, stop_price])
            self.MarketOrder(self.symbol,
                             -int((self.Portfolio.Cash + sum([x.LastFillPrice * x.LastFillQuantity for x in
                                                              filter(lambda y: y.Direction == OrderDirection.Buy,
                                                                     map(lambda z: z.Value,
                                                                         self.Transactions)))) / exit_price))
            
    def OnEndOfDay(self):
         '''Close out any open orders at end of day'''
         orders = list(filter(lambda o: o.Status == OrderStatus.Submitted or o.Status == OrderStatus.PartiallyFilled,
                              map(lambda t: t.Value.Order,
                                  filter(lambda t: t.Value.Symbol == Symbol.Create(self.symbol),
                                         map(lambda t: (t.Key,t.Value),
                                             filter(lambda kvt: isinstance(kvt.Value, qcapi.Order),
                                                    dict.items(self.Transactions)))))))
         for order in orders:
             cancel_order(order.Id)
    
    def ATR(self,symbol):
         '''Calculate Average True Range'''
         period=14
         atr= AverageTrueRange(symbol,self.resolution,self.period)
         return atr