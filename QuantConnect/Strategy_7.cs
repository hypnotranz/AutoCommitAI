

# Momentum_WilliamsR.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import WilliamsPercentR, AverageTrueRange
from datetime import timedelta


class Momentum(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)  
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)  
        
        self.symbol = "SPY"
        self.period = 14
        
        self.williamsR = WilliamsPercentR(self.symbol, self.period)
        self.atr = AverageTrueRange(self.symbol, 14)
        
        self.entryPrice = None
        self.trailingStopPrice = None
        self.stopLossPrice = None
        
        # warm up indicators
        history = self.History(self.symbol, 50 * self.period, Resolution.Daily)
        for bar in history.itertuples():
            tradeBar = TradeBar(bar.Index[0], bar.Symbol, bar.open, bar.high, bar.low, bar.close, bar.volume)
            self.williamsR.Update(tradeBar)
            if not self.atr.IsReady:
                continue
            if tradeBar.Time < history.index[-1] - timedelta(days=14):
                continue
            atrValue = (self.atr.Current.Value * 2) + tradeBar.Close
            if not self.stopLossPrice or atrValue < self.stopLossPrice:
                self.stopLossPrice = atrValue
        
    def OnData(self, data):
        
        if not data.ContainsKey(self.symbol):
            return
        
        if not (self.williamsR.IsReady and self.atr.IsReady):
            return
        
        price = data[self.symbol].Close
        
        # check for exit conditions first 
        if (self.entryPrice and 
            ((self.williamsR.Current.Value > -50 and price < (self.entryPrice * 0.99)) or 
             (self.williamsR.Current.Value < -50 and price > (self.entryPrice * 1.01)) or 
             (price < self.trailingStopPrice))):
            
            orderTicket = None
            
            # close the position
            if(self.Portfolio[self.symbol].IsLong):
                orderTicket = self.MarketOrder(self.symbol, -self.Portfolio[self.symbol].Quantity)
            
            if orderTicket is not None and orderTicket.Status == OrderStatus.Filled:
                fillPrice = orderTicket.AverageFillPrice
                
                # reset variables for next trade
                self.entryPrice = None
                self.trailingStopPrice = None
                
                return
            
        
        # check for entry conditions 
        if (not self.Portfolio.Invested and 
            ((self.williamsR.Current.Value > -20) or 
             (self.williamsR.Current.Value < -80))):
            
            orderTicket = None
            
            
            # enter the position with a market order
            if(self.williamsR.Current.Value > -20):
                orderTicket = self.MarketOrder(self.symbol, int(self.Portfolio.Cash / price))
                
                # set entry price and stop loss price for long positions only
                if orderTicket is not None and orderTicket.Status == OrderStatus.Filled:
                    fillPrice = orderTicket.AverageFillPrice
                    
                    atrValueLongPositionEntry=fillprice-(2*self.atr.Current.Value)
                    atrValueLongPositionExit=fillprice+(2*self.atr.Current.Value)
                    
                    stopLoss=self.MarketOnCloseOrder(symbol=self.Symbol,int(-1*self.Portfolio[self.Symbol].Quantity),stopLoss_LongPosition_Entry,True,"")
                    trailStop=self.StopMarketOrder(symbol=self.Symbol,int(-1*self.Portfolio[self.Symbol].Quantity),0.01,True,"")
                    
                    '''if not stopLoss is None:
                        stopLossTag=stopLoss.OrderTag
                        
                        stopLossTag.exit_time=datetime.now()+timedelta(minutes=30)   
                        
                        trailingStopTag=trailStop.OrderTag
                        
                        trailingStopTag.exit_time=datetime.now()+timedelta(minutes=30)'''
                    
                    '''
                    
                    print("Entry Price: {}".format(fillprice))
                    
                    print("ATR: {}".format(atrValue))
                    
                    print("Trailing Stop Loss: {}".format(trailStop.Price))
                    
                     '''
                
            
          
            
            
    def OnOrderEvent(self,event):
      
        
      '''if event.Status==OrderStatus.Filled:
          
          print(event.OrderId,event.OrderType,event.QuantityFilled,event.FillQuantity,event.Direction,event.SecurityType,event.Symbol,event.Fill.Price,
               event.SecurityIdentifier,event.Status)'''
      
      pass
      
      
    def OnEndOfAlgorithm(self):
        
      pass

   
        
        
        
        
        
        
        
        
        
        


        
        
        
        
        
        
        
        

        
        
        
        


    
        
        
        
        

    
        
    
    



    
    
    
    
    
    



    
        
        
        

    
    

    
    

    
    
    
    


        
            
            
            
                
                

                
                

                
                
                
                
