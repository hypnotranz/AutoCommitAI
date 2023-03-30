

# Momentum.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import WilliamsPercentR, AverageTrueRange
from datetime import timedelta


class Momentum(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)  
        self.SetEndDate(2020, 1, 1)  
        self.SetCash(100000)  
        
        # Define the ticker to trade and the Williams %R indicator
        self.ticker = "SPY"
        self.wpr = WilliamsPercentR(14)
        
        # Define the ATR and trailing stop values
        self.atr = AverageTrueRange(14)
        self.trailing_stop = None
        
        # Define the overbought and oversold levels for entry
        self.overbought_level = -20
        self.oversold_level = -80
        
        # Create a consolidator to group data on a weekly basis
        consolidator = TradeBarConsolidator(timedelta(7))
        
        # Register the consolidator and indicator for updates
        consolidator.DataConsolidated += self.OnDataConsolidated
        self.SubscriptionManager.AddConsolidator(self.ticker, consolidator)
        
    def OnDataConsolidated(self, sender, consolidated):
        
        # Update the Williams %R indicator with new data
        self.wpr.Update(consolidated.Time, consolidated.High,
                         consolidated.Low, consolidated.Close)
        
        # Check for entry signals based on overbought or oversold levels
        if not self.Portfolio[self.ticker].Invested:
            if self.wpr.Current.Value <= self.oversold_level:
                stop_price = consolidated.Low - (2 * self.atr.Current.Value)
                order_size = int(self.Portfolio.Cash / consolidated.Close)
                if order_size > 0:
                    order_ticket = self.MarketOrder(self.ticker, order_size)
                    if order_ticket.Status == OrderStatus.Filled:
                        stop_market_ticket = \
                            self.StopMarketOrder(self.ticker,
                                                 -order_size,
                                                 stop_price)
                        if stop_market_ticket.Status != OrderStatus.Filled:
                            raise ValueError("Stop market order failed to fill")
                        else:
                            # Record the trailing stop price for monitoring purposes
                            self.trailing_stop = stop_price
                    
            elif wpr.Current.Value >= overbought_level:
                stop_price = consolidated.High + (2 * atr.Current.Value)
                order_size = int(self.Portfolio.Cash / consolidated.Close)
                if order_size > 0:
                    order_ticket = \
                        self.LimitOrder(self.ticker,
                                        -order_size,
                                        consolidated.Close)
                    if order_ticket.Status == OrderStatus.Filled:
                        stop_market_ticket = \
                            StopMarketOrder(self.ticker,
                                                order_size,
                                                stop_price)
                        if stop_market_ticket.Status != OrderStatus.Filled:
                            raise ValueError("Stop market order failed to fill")
                        else:
                            # Record the trailing stop price for monitoring purposes
                            self.trailing_stop = stop_price
        
    def OnData(self, data):
        
         # Check for exit signals based on opposite signal or trailing stops 
         current_position_quantity=\
             sum([x.Quantity for x in list(self.Portfolio.Values)])
         current_position_value=\
             sum([x.LastPrice*x.Quantity for x in list(data.Values)])
             
         current_position_profit_loss=\
             sum([x.UnrealizedProfitLoss for x in list(self.Portfolio.Values)])
             
         if current_position_quantity != 0 and \
                 ((self.wpr.Current.Value >= oversold_level and \
                   current_position_quantity > 0) or \
                  (self.wpr.Current.Value <= overbought_level and \
                   current_position_quantity < 0) or \
                  (self.trailing_stop is not None and \
                   ((current_position_value <= trailing_stop and \
                     current_position_quantity > 0) or \
                    (current_position_value >= trailing_stop and \
                     current_position_quantity < 0)))):
                     
                     sell_order_ticket=\
                         MarketOrder(ticker,-current_position_quantity,\
                                     "Exiting existing position")
                     
                     if sell_order_ticket.Status!=OrderStatus.Filled:
                         raise ValueError("Sell market order failed to fill")
                     
         elif current_position_quantity==0:  
             pass 
             
         else: 
             logging.error(f"Unexpected position {current_position_value}")
             assert(False)