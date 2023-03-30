

# Momentum_CCI.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import CommodityChannelIndex
from QuantConnect.Algorithm.Framework import QCAlgorithmFramework
from QuantConnect.Algorithm.Framework.Execution import ExecutionModel
from QuantConnect.Algorithm.Framework.Portfolio import EqualWeightingPortfolioConstructionModel
from QuantConnect.Algorithm.Framework.Risk import MaximumDrawdownPercentPerSecurity
from datetime import timedelta


class Momentum(QCAlgorithmFramework):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)

        self.AddEquity("SPY", Resolution.Daily)

        self.cci = self.INDICATOR(CommodityChannelIndex, "SPY", 20)
        self.previous = None

        # Set up portfolio construction and risk management models
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.01))

    def OnData(self, data):
        
        if not (data.ContainsKey("SPY") and data["SPY"] and data["SPY"].Close):
            return
        
        current = data["SPY"].Close
        
        if not (self.previous and current):
            return
        
        holdings = sum([x.Value.Holdings.Quantity for x in self.Portfolio.Values])
        
        if holdings == 0:
            if self.cci.Current.Value > 100:
                # Buy signal above 100 level
                quantity = int(self.Portfolio.TotalPortfolioValue / current)
                order = self.Order("SPY", quantity)
                
                # Set stop loss at 1 x ATR below entry price
                atr = self.ATR("SPY", 20).Current.Value
                stopPrice = current - atr
                order.StopMarket(stopPrice)

            elif self.cci.Current.Value < -100:
                # Short signal below -100 level
                quantity = int(self.Portfolio.TotalPortfolioValue / current)
                order = self.Order("SPY", -quantity)
                
                # Set stop loss at 1 x ATR above entry price
                atr = self.ATR("SPY", 20).Current.Value
                stopPrice = current + atr
                order.StopMarket(stopPrice)

            else:
                return
                
            # Set previous price for next iteration    
            self.previous = current
            
        
        elif holdings > 0:
            
            if (self.cci.Current.Value < -100) or (current < order.StopPrice):
                
                # Sell signal or trailing stop loss triggered    
                sellQuantity = int(self.Portfolio.TotalPortfolioValue / current)
                
                if sellQuantity == holdings:
                    # Liquidate all shares if no partial sells allowed 
                    order.Liquidate()
                    
                    # Reset previous price for next iteration    
                    self.previous = None
                
                
        
        elif holdings < 0:
            
            if (self.cci.Current.Value > 100) or (current > order.StopPrice):
                
                 # Buy signal or trailing stop loss triggered    
                 buyQuantity= int(self.Portfolio.TotalPortfolioValue / current)
                 
                 if buyQuantity == abs(holdings):
                     # Liquidate all shares if no partial buys allowed 
                     order.Liquidate()
                     
                     # Reset previous price for next iteration    
                     self.previous = None
                
        
    def OnOrderEvent(self, orderEvent):
        
        if not(orderEvent.Status == OrderStatus.Filled or 
               orderEvent.Status == OrderStatus.PartiallyFilled): 
             return
        
         fillQuantity=orderEvent.FillQuantity
        
         fillPrice=orderEvent.FillPrice
        
         if fillQuantity>0: 
            
             buyOrder=self.Transactions.GetOrderById(orderEvent.OrderId) 
            
             stopLossPrice=fillPrice-self.ATR("SPY",20).Current.Value
            
             buyOrder.StopMarket(stopLossPrice) 
        
         elif fillQuantity<0: 
            
             sellOrder=self.Transactions.GetOrderById(orderEvent.OrderId) 
            
             stopLossPrice=fillPrice+self.ATR("SPY",20).Current.Value
            
             sellOrder.StopMarket(stopLossPrice)