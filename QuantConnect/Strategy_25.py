

# TrendFollowing.py

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Orders import * 

class TrendFollowing(QCAlgorithm):

    def Initialize(self):
        
        self.SetStartDate(2010, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 1, 1)    # Set End Date
        self.SetCash(100000)           # Set Strategy Cash
        
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.lr = self.LINEARREG(self.symbol, 50)
        
        self.atr = self.ATR(self.symbol, 14)
        
        self.SetWarmUp(50)
        
    def OnData(self, data):
        
        if not (self.lr.IsReady and self.atr.IsReady): return
        
        current_price = data[self.symbol].Close
        
        if not self.Portfolio.Invested:
            
            if current_price > self.lr.Current.Value and current_price > (self.lr.Current.Value + (self.atr.Current.Value)):
                
                stop_price = current_price - (self.atr.Current.Value)
                
                quantity = int(self.Portfolio.Cash / current_price)
                
                self.StopMarketOrder(self.symbol, -quantity, stop_price)
                
                self.MarketOrder(self.symbol, quantity)
                
        else:
            
            open_orders = [x for x in self.Transactions.GetOpenOrders() if x.Symbol == self.symbol]
            
            if open_orders: return
            
            if current_price < (self.lr.Current.Value - (self.atr.Current.Value)):
                
                stop_loss_order = StopMarketOrder(self.symbol, -self.Portfolio[self.symbol].Quantity,
                                                 (self.Portfolio[self.symbol].AveragePrice - (self.atr.Current.Value)),
                                                 "Stop Loss")
                
            elif current_price < ((self.lr.Current.Value - (0.01 * current_price))):

                sell_order = MarketOrder(self.symbol, -self.Portfolio[self.symbol].Quantity,
                                         "Take Profit")
            
    def OnOrderEvent(self, orderEvent):
        
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        
        if order.Type == OrderType.StopMarket and orderEvent.Status == OrderStatus.Filled:
            
            sell_order = MarketOrder(self.symbol, -order.Quantity,
                                     "Stop Loss")
            
    def OnEndOfAlgorithm(self):
        
        positions = list(self.Portfolio.Values)
        
        for position in positions:
            
            if position.Invested:
                
                sell_order = MarketOrder(position.Symbol,
                                         -position.Quantity,
                                         "End of Algorithm")