

# Strategy_TrendFollowing.py

from datetime import timedelta
import numpy as np

class TrendFollowing(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2021, 12, 31)
        self.SetCash(100000)
        
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.fast_period = 10
        self.slow_period = 30
        self.atr_period = 14
        
        # Set up AMA indicators
        self.fast_ama = AdaptiveMovingAverage(self.fast_period)
        self.slow_ama = AdaptiveMovingAverage(self.slow_period)
        
        # Set up ATR indicator
        self.atr = AverageTrueRange(self.atr_period)
        
        # Schedule our function to fire at the start of each trading day
        self.Schedule.On(self.DateRules.EveryDay(self.symbol), 
                         self.TimeRules.At(9, 30), 
                         Action(self.EveryDay))
    
    def EveryDay(self):
        
        # Get historical data to calculate AMA indicators and ATR
        historical_data = self.History([self.symbol], 
                                       max(self.fast_period, 
                                           max(self.slow_period, 
                                               self.atr_period)), 
                                       Resolution.Daily).close
        
        # Calculate AMA indicators
        fast_ama_values = np.array([self.fast_ama.UpdateValue(x) for x in historical_data])
        slow_ama_values = np.array([self.slow_ama.UpdateValue(x) for x in historical_data])
        
        # Calculate ATR
        atr_value = self.atr.Current.Value
        
         # Check if we have enough data to trade
         if not all(np.isnan(fast_ama_values[-2:])) and not all(np.isnan(slow_ama_values[-2:])):
            
            current_price = historical_data[-1]
            previous_price = historical_data[-2]
            
            current_fast_ama_value = fast_ama_values[-1]
            previous_fast_ama_value = fast_ama_values[-2]
            
            current_slow_ama_value= slow_ama_values[-1]
            previous_slow_ama_value= slow_ama_values[-2]
            
            position_size= int(self.Portfolio.TotalPortfolioValue / current_price)
            
            if previous_price < previous_fast_ama_value and current_price > current_fast_ama_value:
                # Buy entry signal
                
                stop_loss_price= current_price - atr_value
                
                # Submit buy order with stop loss order attached
                order_ticket= None
                
                if not self.Portfolio[self.symbol].Invested:
                    order_ticket= \
                    self.MarketOrder(
                        symbol=self.symbol,
                        quantity=position_size,
                        tag="Buy Entry",
                        stopLossPrice=stop_loss_price,
                        expiration=self.Time + timedelta(minutes=5))
                
                    if order_ticket is not None and order_ticket.Status != OrderStatus.Filled:
                        return
                
            elif previous_price > previous_slow_ama_value and current_price < current_slow_ama_value:
                
                # Sell entry signal
                
                stop_loss_price= current_price + atr_value
                
                # Submit sell order with stop loss order attached 
                order_ticket=None
                
                if not self.Portfolio[self.symbol].Invested:
                    order_ticket=self.MarketOrder(
                                    symbol=self.symbol,
                                    quantity=-position_size,
                                    tag="Sell Entry",
                                    stopLossPrice=stop_loss_price,
                                    expiration=self.Time+timedelta(minutes=5))
                
                    if order_ticket is not None and \
                    (order_ticket.Status==OrderStatus.Invalid or\
                     (order_ticket.Status!=OrderStatus.Filled and\
                      order_ticket.Status!=OrderStatus.PartiallyFilled)):
                            return
                        
           elif (self.Portfolio[self.symbol].IsLong or \
             (order_ticket is not None and \
              (order_ticket.Status==OrderStatus.Submitted or\
               order_ticket.Status==OrderStatus.PartiallyFilled)))\
              and current_price<=current_slow_ma:            
                  
              # Exit long position signal    
              sell_order=None
            
              if not any(x.Tag == "Sell Exit" for x in self.Transactions.GetOpenOrders()):
                  sell_order=self.MarketOrder(
                          symbol=self.symbol,
                          quantity=-self.Portfolio[self.symbol].Quantity,
                          tag="Sell Exit",
                          expiration=self.Time+timedelta(minutes=5))
              
                  if sell_order is not None and \
                     (sell_order.Status==OrderStatus.Invalid or\
                      (sell_order.Status!=OrderStatus.Filled and\
                       sell_order.Status!=OrderStatus.PartiallyFilled)):
                      return
            
           elif (self.Portfolio[self.symbol].IsShort or \
             (order_ticket is not None and \
              (order_ticket.Status==OrderStatus.Submitted or\
               order_tick