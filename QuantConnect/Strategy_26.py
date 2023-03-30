

# Strategy_SupportResistance.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import PivotPoints, ExponentialMovingAverage, AverageTrueRange
from datetime import timedelta


class SupportResistance(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  
        self.SetEndDate(2020, 12, 31)  
        self.SetCash(100000)  
        
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Indicators
        self.pivot = PivotPoints("SPY")
        self.ema = ExponentialMovingAverage(30)
        self.atr = AverageTrueRange(14)
        
        # Set warmup period
        self.SetWarmUp(timedelta(days=30))
        
    def OnData(self, data: TradeBar):
        
        if not (self.pivot.IsReady and self.ema.IsReady and self.atr.IsReady):
            return
        
        # Check if price is at pivot point
        if data.Close == self.pivot.Resistance1:
            # Buy on breakout above pivot point with ATR stop loss
            stop_price = data.Close - (self.atr.Current.Value * 1)
            self.SetStopLoss(self.symbol, stop_price)
            self.MarketOrder(self.symbol, 100)
            
        elif data.Close == self.pivot.Support1:
            # Short on breakdown below pivot point with ATR stop loss
            stop_price = data.Close + (self.atr.Current.Value * 1)
            self.SetStopLoss(self.symbol, stop_price)
            self.MarketOrder(self.symbol, -100)
            
        
    def OnOrderEvent(self, orderEvent):
        
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        
        if order.Status != OrderStatus.Filled:
            return
        
        # Exit on opposite signal or trailing stop
        position = [x for x in self.Portfolio if x.Key == order.Symbol][0].Value
        if position.Quantity > 0:
            exit_price = min(self.pivot.Support2, max(order.Price - (self.atr.Current.Value * 2), 
                                                      position.AveragePrice * (1 - 0.02)))
            if exit_price < data.Close:
                return
                
            limit_order = self.LimitOrder(order.Symbol, -position.Quantity,
                                          exit_price,
                                          "Exit Buy")
            
    
            
                
        
        
        
        
        
        
        