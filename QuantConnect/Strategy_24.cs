

# Strategy_TrendFollowing.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import ZigZag
from QuantConnect.Orders import OrderDirection, StopMarketOrder
from datetime import timedelta


class TrendFollowing(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)
        self.AddEquity("SPY", Resolution.Daily)
        
        self.stop = 2 * AverageTrueRange("SPY", 14)
        self.trailing_stop = None
        
        self.zigzag = ZigZag(0.05)
        
    def OnData(self, data: TradeBar):
        if not self.zigzag.IsReady:
            return
        
        if self.Portfolio.Invested and (self.zigzag.Current.Value == -1 or data.Close < self.trailing_stop):
            # Exit position
            self.Liquidate()
            
        elif not self.Portfolio.Invested and self.zigzag.Current.Value == 1:
            # Enter long position
            stop_price = data.Close - self.stop
            take_profit_price = data.Close + (2 * (data.Close - stop_price))
            
            stop_order = StopMarketOrder("SPY", -self.Portfolio.Cash / data.Close, stop_price)
            take_profit_order = LimitOrder("SPY", -self.Portfolio.Cash / data.Close, take_profit_price)
            
            self.trailing_stop = stop_price
            
            # Submit both orders simultaneously
            if not (stop_order.Status == OrderStatus.Filled or take_profit_order.Status == OrderStatus.Filled):
                # Submit both orders together so we only enter the position if both are successful
                ticket_group = [self.SumbitOrder(stop_order),self.SubmitOrder(take_profit_order)]
                for ticket in ticket_group:
                    if ticket.Status != OrderStatus.Filled:
                        return
                
                # Update trailing stop as soon as we enter the position
                history_request = HistoryRequest("SPY", timedelta(days=5), Resolution.Hour)
                history_data = History(history_request).loc["SPY"].iloc[-1]
                
                high_since_entry = history_data.High
                
                while True:
                    current_data = History(history_request).loc["SPY"].iloc[-1]
                    
                    if current_data.High > high_since_entry:
                        high_since_entry = current_data.High
                        
                    trailing_stop_update_price = high_since_entry - self.stop
                    
                    if trailing_stop_update_price > self.trailing_stop:
                        # Update the trailing stop and break out of the loop
                        update_result_ticket=self.StopMarketOrder("SPY", -self.Portfolio.Cash / data.Close, trailing_stop_update_price)
                        if update_result_ticket.Status != OrderStatus.Filled:
                            return
                        
                        break
                    
                    time.sleep(60)