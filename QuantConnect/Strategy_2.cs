

# Momentum_RSI_Strategy.py

from QuantConnect.Data import SubscriptionDataSource
from QuantConnect.Python import PythonData
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Indicators import RelativeStrengthIndex
from QuantConnect.Orders import OrderStatus, OrderType, TimeInForce
from QuantConnect.Data.Market import TradeBar


class Momentum(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  
        self.SetEndDate(2020, 12, 31)  
        self.SetCash(100000)  
        self.AddEquity("SPY", Resolution.Daily)
        
        # Relative Strength Index indicator with period of 14 and overbought/oversold levels of 70/30 
        self.rsi = self.RSI("SPY", 14, MovingAverageType.Simple, Resolution.Daily)
        
        # Initialize trailing stop value to None
        self.trailingStop = None
        
    def OnData(self, data):
        
        if not self.rsi.IsReady:
            return
        
        if not self.Portfolio.Invested:
            if self.rsi.Current.Value > 70:
                # If the RSI is overbought and we're not invested, send a market order for the maximum number of shares possible.
                self.MarketOrder("SPY", int(self.Portfolio.Cash / data["SPY"].Close))
                
                # Set trailing stop loss at 1.5 * ATR (average true range)
                atr = self.ATR("SPY", 14)
                self.trailingStop = data["SPY"].Close - (1.5 * atr.Current.Value)
                
        else:
            if data["SPY"].Close <= self.trailingStop:
                # If the current price is below the trailing stop loss value,
                # sell all shares we're holding with a market order.
                self.MarketOrder("SPY", -self.Portfolio["SPY"].Quantity)
                
            elif (self.rsi.Current.Value < 30) and (self.Transactions.GetOpenOrders().Count == 0):
                # If the RSI is oversold and we don't have any open orders,
                # sell all shares we're holding with a market order.
                self.MarketOrder("SPY", -self.Portfolio["SPY"].Quantity)