

# Strategy_TrendFollowing.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import DonchianChannel
from datetime import timedelta

class TrendFollowing(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        self.AddEquity("SPY", Resolution.Daily)

        # Initialize Donchian Channel
        self.dc = DonchianChannel(20)

        # Initialize ATR
        self.atr = self.ATR("SPY", 20, MovingAverageType.Simple, Resolution.Daily)

        # Initialize last trade time and price
        self.lastTradeTime = None
        self.lastTradePrice = None

    def OnData(self, data: TradeBar):
        
        # Wait for Donchian Channel to fully initialize
        if not self.dc.IsReady:
            return

        if not self.Portfolio.Invested:
            if data.Close > self.dc.UpperBand.Current.Value:
                # Buy when price breaks above upper band of Donchian Channel
                self.SetHoldings("SPY", 1.0)
                self.lastTradeTime = data.Time
                self.lastTradePrice = data.Close

            elif data.Close < self.dc.LowerBand.Current.Value:
                # Short when price breaks below lower band of Donchian Channel
                self.SetHoldings("SPY", -1.0)
                self.lastTradeTime = data.Time
                self.lastTradePrice = data.Close
        
        else:
            # Check for exit criteria
            
            if (self.Portfolio.Invested > 0 and data.Close < self.dc.LowerBand.Current.Value) or (self.Portfolio.Invested < 0 and data.Close >self.dc.UpperBand.Current.Value):
                # Opposite signal received, exit position 
                if (self.Portfolio.Invested > 0):
                    # Long position to exit 
                    stopPrice = max(self.lastTradePrice - (self.atr.Current.Value),data.Low)
                    orderTicket=self.StopMarketOrder("SPY",-self.Portfolio["SPY"].Quantity,stopPrice)
                    if orderTicket is not None and orderTicket.Status==OrderStatus.Filled:
                        Log(f"Exit long position at {orderTicket.AverageFillPrice} on {data.Time}")
                        return 
                    
                
                elif (self.Portfolio.Invested < 0):
                    # Short position to exit 
                    stopPrice = min(self.lastTradePrice + (self.atr.Current.Value),data.High) 
                    orderTicket=self.StopMarketOrder("SPY",-self.Portfolio["SPY"].Quantity,stopPrice) 
                    
                    if orderTicket is not None and orderTicket.Status==OrderStatus.Filled:
                        Log(f"Exit short position at {orderTicket.AverageFillPrice} on {data.Time}")
                        return 

            else:
                
                 ## Trailing Stop Loss - Long Position
                
                
                 if (self.Portfolio.Invested > 0):   
                     
                     stopLoss= max(self.lastTradePrice - (1 *self.atr.Current.Value),data.Low)

                     ## Check trailing stop loss condition                 
                     if(data.Low < stopLoss):               
                     
                         orderTicket=self.StopMarketOrder("SPY",-self.Portfolio["SPY"].Quantity,stopLoss) 
                         
                         if orderTicket is not None and orderTicket.Status==OrderStatus.Filled:
                            Log(f"Stop Loss Triggerred for long position at {orderTicket.AverageFillPrice} on {data.Time}")
                            return 

                 ## Trailing Stop Loss - Short Position
                
                 elif (self.Portfolio.Invested < 0):   
                     
                     stopLoss= min(self.lastTradePrice + (1 *self.atr.Current.Value),data.High)

                     ## Check trailing stop loss condition                 
                     if(data.High > stopLoss):               
                     
                         orderTicket=self.StopMarketOrder("SPY",-self.Portfolio["SPY"].Quantity,stopLoss) 
                         
                         if orderTicket is not None and orderTicket.Status==OrderStatus.Filled:
                            Log(f"Stop Loss Triggerred for short position at {orderTicket.AverageFillPrice} on {data.Time}")
                            return 

        
    def OnEndOfDay(self):
        
         ## Update the last trade price when there are no trades during the day.
         
         holdings=self.Securities["SPY"].Holdings
        
         if holdings is not None and holdings.Quantity!=0:            
             ## Update the last trade time when there are no trades during the day.
             lastbar=self.History(["SPY"],2).iloc[0]             
             symbol="SPY"
             last_price=lastbar.loc[symbol]['close']           
             
             ## Update the