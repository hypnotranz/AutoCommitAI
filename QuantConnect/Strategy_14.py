

# Volume_Strategy.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import PriceVolumeTrend
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Orders import OrderDirection, StopMarketOrder


class Volume(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.pvt = PriceVolumeTrend(self.symbol, 14)
        self.atr = self.ATR(self.symbol, 14)

    def OnData(self, data: TradeBar):
        
        # Check for buy signal
        if not self.Portfolio.Invested and self.pvt.Current.Value > 0 and \
            self.pvt.Current.Value > self.pvt.Signal.Current.Value:
            quantity = int(self.Portfolio.Cash / data.Close)
            stop_price = data.Close - (self.atr.Current.Value * 1)
            self.MarketOrder(self.symbol, quantity)
            self.stop_loss_order = StopMarketOrder(self.symbol, -quantity,
                                                   stop_price)

        # Check for sell signal or stop loss hit
        elif self.Portfolio.Invested and (self.pvt.Current.Value < 0 or 
                                          data.Close < 
                                          self.stop_loss_order.StopPrice):
            if data.Close < \
                max([x.AveragePrice for x in 
                     self.Transactions.GetOpenOrders()]):
                return

            quantity = abs(int(self.Portfolio[self.symbol].Quantity))
            if not data.Close < \
                (self.pvt.Signal.Current.Value + 
                 (self.atr.Current.Value * 0.5)):
                stop_price = data.Close + (self.atr.Current.Value * 1)
                stop_loss_order = StopMarketOrder(self.symbol,
                                                  -quantity,
                                                  stop_price)

            # Sell all shares if opposite signal
            else:
                stop_loss_order.Cancel()
                sell_order = marketOrder(self.symbol, -quantity)