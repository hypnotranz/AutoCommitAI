

# Strategy_SupportResistance.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import PivotPoints, RollingWindow
from datetime import timedelta


class SupportResistance(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)
        self.AddEquity("SPY", Resolution.Daily)
        
        # Create indicators
        self.pp = PivotPoints("PP", 14)
        
        # Rolling window for price history
        self.window = RollingWindow[TradeBar](2)
        
        # Initialize variables
        self.entryPrice = None
        self.stopPrice = None
        self.exitPrice = None
    
    def OnData(self, data):
        
        if not (data.ContainsKey("SPY") and data["SPY"].Close):
            return
        
        # Add new data to rolling window
        self.window.Add(data["SPY"])
        
        # Wait for enough data to calculate pivot points
        if not all(map(lambda x: x.IsReady, [self.pp])):
            return
        
        # If we have a position and the price has reached the pivot point, exit the position
        if self.Portfolio.Invested:
            if (self.entryPrice < self.pp.Support2 and data["SPY"].Close > self.pp.Support2) or \
                    (self.entryPrice > self.pp.Resistance2 and data["SPY"].Close < self.pp.Resistance2):
                self.Liquidate()
                return
            
            if (self.entryPrice < self.pp.Support1 and data["SPY"].Close > self.exitPrice) or \
                    (self.entryPrice > self.pp.Resistance1 and data["SPY"].Close < self.exitPrice):
                return
            
            if data["SPY"].Close > max(self.exitPrice, max(self.window[0].High, 
                                                            max(self.window[0].Low + ATR("ATR", 14).Current.Value,
                                                                max(self.window[1].High - ATR("ATR", 14).Current.Value,
                                                                    max(self.pp.Resistance1 + ATR("ATR", 14).Current.Value,
                                                                        max(self.pp.Resistance2 + ATR("ATR", 14).Current.Value,
                                                                            max(self.pp.Resistance3 + ATR("ATR", 14).Current.Value,
                                                                                max(self.pp.Resistance4 + ATR("ATR", 14).Current.Value,
                                                                                    max(self.pp.Resistance5 + ATR("ATR", 14).Current.Value,
                                                                                        -float('inf')))))))))):
                return
            
            else:
                stopLoss = StopMarketOrder("StopLossOrder", -self.Portfolio[self.Symbol].Quantity, 
                                           min(data["SPY"].Low - ATR("ATR", 14).Current.Value, 
                                               min(min(self.window[0].Low,self.window[1].Low))))
                
                stopLossTag = "{}-{}".format(stopLoss.TypeName.lower(), stopLoss.Id)
                if not stopLossTag in [x.Tag for x in list(self.Transactions.GetOpenOrders())]:
                    submitResult = self.SubmitOrder(stopLoss)
                    stopLossTicket = submitResult.OrderTicket
                    
                    if stopLossTicket is not None:
                        stopLossTicket.UpdateTag(stopLossTag)

                
            
    
    def OnOrderEvent(self, orderEvent):
        
    def SetStopAndExitPrices(self):
        
            
    def RebalancePortfolio(self):