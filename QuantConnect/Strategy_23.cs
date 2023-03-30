

# Strategy_TrendFollowing.py

from QuantConnect.Data import *
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import *
from QuantConnect.Algorithm.Framework import *

class TrendFollowing(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 31)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash

        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.supertrend = self.SuperTrend(self.symbol, 10)
        self.atr = self.ATR(self.symbol, 14)

        # Set up trailing stop
        self.trailing_stop = None

        # Buy/Sell signals
        self.buy_triggered = False
        self.sell_triggered = False

    def OnData(self, data):
        if not (self.supertrend.IsReady and data.ContainsKey(self.symbol)):
            return

        price = data[self.symbol].Close

        if price > self.supertrend.UpperBand.Current.Value and not self.buy_triggered:
            # Buy signal - price crosses upper band
            stop_price = price - (self.atr.Current.Value * 1)
            limit_price = None  # No limit order

            # Place order and set up trailing stop
            order_ticket = self.MarketOrder(self.symbol, 100)
            if order_ticket.Status == OrderStatus.Filled:
                stop_price_str = '{:.2f}'.format(stop_price)
                trailing_stop_info = TrailingStopRiskManagementModel.ExitAtStopPrice(order_ticket.OrderId, Decimal(stop_price_str))
                self.trailing_stop = QuantityTrailingStopRiskManagementModel(trailing_stop_info)

                # Reset buy/sell triggers
                self.buy_triggered = True
                self.sell_triggered = False

        elif price < self.supertrend.LowerBand.Current.Value and not sell_triggered:
            # Sell signal - price crosses lower band or stop loss triggered by trailing stop
            stop_price = None  # No stop loss order since trailing stop is in place
            limit_price = None  # No limit order

            # Place order and cancel existing trailing stop (if any)
            order_ticket = self.MarketOrder(self.symbol, -100)
            if order_ticket.Status == OrderStatus.Filled:
                if (self.trailing_stop is not None):
                    if not (self.trailing_stop.Cancel(order_ticket.OrderId)):
                        return

                # Reset buy/sell triggers
                sell_triggered=True 
                buy_triggered=False