

# Strategy_Volume.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import VolumePriceTrend
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Orders import OrderDirection, StopMarketOrder
from datetime import timedelta

class Volume(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)  
        self.SetEndDate(2020, 1, 1)  
        self.SetCash(100000) 
        self.symbol = self.AddEquity("AAPL", Resolution.Daily).Symbol
        
        self.vpt = VolumePriceTrend("VPT", 14)
        
        self.previous = None
        self.stopMarketTicket = None
        
    def OnData(self, data: TradeBar):
        
        if not self.vpt.IsReady:
            return
        
        if not self.Portfolio.Invested:
            if self.vpt.Current.Value > 0 and (self.previous is None or self.previous < 0):
                # Buy on signal line cross
                quantity = int(self.Portfolio.Cash / data.Close)
                stopPrice = data.Close - (self.ATR(self.symbol, 14).Current.Value * 1)
                self.stopMarketTicket = self.StopMarketOrder(self.symbol, -quantity, stopPrice)
                self.MarketOrder(self.symbol, quantity)
                
        elif data.Close < (self.Portfolio[self.symbol].AveragePrice * .98) or (self.vpt.Current.Value < 0 and (self.previous is None or self.previous > 0)):
            # Sell on opposite signal or trailing stop
            if not self.stopMarketTicket.CancelPending:
                return
                
            if not self.stopMarketTicket.IsActive:
                stopPrice = max(data.Low, (self.Portfolio[self.symbol].AveragePrice * .98))
                updatedStopMarketTicket = StopMarketOrder(self.stopMarketTicket.OrderId, -self.stopMarketTicket.Quantity, stopPrice)
                
                if updatedStopMarketTicket.Status == OrderStatus.Filled:
                    # Cancel the original stop market order
                    cancelResult = self.Transactions.CancelOrder(self.stopMarketTicket.OrderId)
                    if cancelResult.Status == OrderStatus.Cancelled:
                        # Replace the original order with the updated one
                        updateResult = self.Transactions.AddOrder(updatedStopMarketTicket)
                        if updateResult.Status == OrderStatus.Submitted:
                            # Save the new ticket as the current ticket for this position.
                            # This will allow us to check its status on next bar.
                            currentStopMarketTicket = updatedStopMarketTicket