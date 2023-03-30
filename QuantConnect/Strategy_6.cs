

# Momentum.py
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import CommodityChannelIndex, RollingWindow
from datetime import timedelta

class Momentum(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2021, 8, 31)
        self.SetCash(100000)
        self.symbol = "SPY"
        self.AddEquity(self.symbol, Resolution.Daily)
        
        self.cci = CommodityChannelIndex(14)
        self.window = RollingWindow[TradeBar](2)
        
        self.stopMarketTicket = None
        self.entryPrice = None
        self.trailStopPrice = None
        
    def OnData(self, data):
        if not data.ContainsKey(self.symbol) or not data[self.symbol].HasData:
            return
        
        currentBar = data[self.symbol]
        
        # Update the indicators and rolling window with the current bar.
        self.cci.Update(currentBar.EndTime, currentBar.Close)
        
        if not (self.cci.IsReady and len(self.window) == 2):
            return
        
         # Check if we currently have a position
        if not self.Portfolio.Invested:
            if (self.cci.Current.Value > 100 and 
                self.window[0].Close > self.window[1].Close):
                
                # Buy the asset and set stop loss order.
                entryPrice = currentBar.Close
                stopMarketTicket = self.StopMarketOrder(
                    symbol=self.symbol,
                    quantity=self.CalculateOrderQuantity(self.symbol, 0.95),
                    stopPrice=entryPrice - (self.ATR(self.symbol, 14).Current.Value * 1),
                    tag="Stop Loss"
                )
                
                # Set trailing stop order with initial parameters.
                trailStopTicket = self.TrailingStopMarketOrder(
                    symbol=self.symbol,
                    quantity=self.Portfolio[self.symbol].Quantity,
                    trailingStopAmount=self.ATR(self.symbol, 14).Current.Value * 2,
                    tag="Trailing Stop"
                )
                
                # Store entry price and ticket for later reference.
                self.entryPrice = entryPrice
                self.stopMarketTicket = stopMarketTicket
                return
            
            elif (self.cci.Current.Value < -100 and 
                  self.window[0].Close < self.window[1].Close):
                  
                  # Short the asset and set stop loss order.
                  entryPrice = currentBar.Close
                  stopMarketTicket = self.StopMarketOrder(
                      symbol=self.symbol,
                      quantity=self.CalculateOrderQuantity(self.symbol, -0.95),
                      stopPrice=entryPrice + (self.ATR(self.Symbol, 14).Current.Value * 1),
                      tag="Stop Loss"
                  )
                  
                  # Set trailing stop order with initial parameters.
                  trailStopTicket = TrailingStopMarketOrder(
                      symbol=self.Symbol,
                      quantity=self.Portfolio[self.Symbol].Quantity * -1,
                      trailingStopAmount=self.ATR(Symbol, 14).Current.Value *2,
                      tag="Trailing Stop"
                  )
                  
                  # Store entry price and ticket for later reference.
                  entryPrice = currentBar.Close
                  stopMarketTicket = stopMarketTicket   
        
         else:
             # Check exit conditions.
             if ((self.Portfolio[self.Symbol].IsLong and 
                 ((self.cci.Current.Value < -100 and 
                   (currentBar.Close < max([x.Close for x in window])))) or 
                 (self.Portfolio[self.Symbol].IsShort and 
                 ((self.cci.Current.Value >100)and(currentbar.close>min([x.close for x in window]))))):
                 
                 # Close position and cancel pending orders.
                 cancelOrdersResult=CancelOpenOrders()
                 
                 if cancelOrdersResult.IsSuccess:
                     selling_price=currentbar.close
                     position_qty=-self.Portfolio[self.Symbol].Quantity \
                         if Portfolio[self.Symbol] .IsShort else Portfolio [symbol] .Quantity                     
                     limit_price=selling_price \
                         +position_qty*(entry_price-self.stop_loss.Price)/abs(position_qty) \
                         if Portfolio[symbol] .IsLong else selling_price \
                         +position_qty*(entry_price+stop_loss.Price)/abs(position_qty)                     
                     
                     limit_price=max(limit_price,currentbar.Low) \
                         if Portfolio[symbol] .IsLong else min(limit_price,currentbar.High)
                     
                     ticket=LimitOrder(symbol,self.CalculateOrderQuantity(symbol,-0.5*position_qty),limit_price,"Exit")\
                        if Portfolio[symbol] .IsLong else LimitOrder(symbol,self.CalculateOrderQuantity(symbol,-position_qty),limit_price,"Exit")
                        
                        
                    
                
                
                 
                
                
                
             
             
             
             
             
             
             
             
             
        
        
                
                
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



        

    
        
        
        
        
        
        
        
        
