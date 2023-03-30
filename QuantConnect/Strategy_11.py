

# Momentum_Strategy.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import *
from QuantConnect.Orders import *
from QuantConnect.Data.Consolidators import *
import numpy as np


class Momentum(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2019, 1, 1)  
        self.SetEndDate(2021, 5, 31)  
        self.SetCash(100000) 
        self.AddEquity("SPY", Resolution.Minute)
        self.Consolidate("SPY", timedelta(minutes=30), self.OnDataConsolidated)
        
        # Indicator
        self.indicator = ElderRayIndex("SPY", 13, MovingAverageType.Simple, Resolution.Minute)
        
        # Stop loss
        self.atr = AverageTrueRange("SPY", 14)
        
        # Order management
        self.entryPrice = None
        self.entryTime = None
        self.stopPrice = None
        
    def OnData(self, data: TradeBar):
        
        if not (self.indicator.IsReady):
            return

        
        if not (self.Portfolio.Invested) and (self.indicator.Current.Value > 0):
            stop_loss_perc = 0.95
            
            # Entry Criteria
            limitPrice = data.Close
            stopPrice = limitPrice * stop_loss_perc
            
            # Record entry values for use later in exit criteria.
            self.entryTime = data.Time
            self.entryPrice = limitPrice
            
            # Set Stop Loss Order.
            quantity = np.floor(self.Portfolio.Cash / limitPrice)
            
            stop_loss_ticket=self.StopMarketOrder("SPY", -quantity, stopPrice)

            
            # Set Entry Order.
            orderTicket=self.LimitOrder("SPY", quantity, limitPrice)

        
    def OnDataConsolidated(self,sender,args):
        
      if not (self.indicator.IsReady):
          return
      
      # Exit Criteria
      
      if (self.Portfolio.Invested and ((self.Time - self.entryTime).days > 0)):
          
          current_price=self.Securities["SPY"].Close
            
          if current_price < (self.entryPrice - (1 * float(self.atr.Current.Value))):
              self.Liquidate()
              return          
          
          elif current_price > (self.entryPrice + float(self.atr.Current.Value)):
              stop_loss_perc=0.95
                
              limit_price=current_price
              stop_price=limit_price*stop_loss_perc
                
              quantity=np.floor(self.Portfolio.Cash/limit_price)
                
              order_ticket=self.StopMarketOrder("SPY",-quantity,stop_price) 
            
          elif ((not (self.indicator.Current.Value > 0)) and 
                ((current_price < self.entryPrice) or 
                 ((current_price - float(self.atr.Current.Value)) < 
                  max(stop_loss_ticket.AverageFillPrice,self.stopPrice)))):
                    
                self.Liquidate()