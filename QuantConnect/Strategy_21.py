

# Momentum_Trix.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import Trix
from QuantConnect.Algorithm.Framework.Alphas import InsightDirection
from QuantConnect.Algorithm.Framework.Selection import ManualUniverseSelectionModel
from QuantConnect.Algorithm.Framework.Execution import ImmediateExecutionModel
from QuantConnect.Algorithm.Framework.Portfolio import EqualWeightingPortfolioConstructionModel
from QuantConnect.Algorithm.Framework.Risk import MaximumDrawdownPercentPerSecurity, NullRiskManagementModel

class MomentumTrix(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        
        # Add universe of securities to be traded
        symbols = [Symbol.Create("AAPL", SecurityType.Equity, Market.USA),
                   Symbol.Create("GOOGL", SecurityType.Equity, Market.USA),
                   Symbol.Create("MSFT", SecurityType.Equity, Market.USA),
                   Symbol.Create("AMZN", SecurityType.Equity, Market.USA),
                   Symbol.Create("FB", SecurityType.Equity, Market.USA)]
        
        self.UniverseSettings.Resolution = Resolution.Daily
        
        # Set up data subscriptions and indicators for each security in the universe
        for symbol in symbols:
            self.AddEquity(symbol)
            trix = self.TRIX(symbol, 14)
            trix_signal = self.TRIX(symbol, 7)
            
            # Add indicators to the security's data dictionary
            symbol_data = self.Securities[symbol]
            symbol_data.Trix = trix
            symbol_data.TrixSignal = trix_signal
            
        # Use ManualUniverseSelectionModel to select securities in the universe to trade    
        self.SetUniverseSelection(ManualUniverseSelectionModel(symbols))
        
        # Use ImmediateExecutionModel for order execution 
        self.SetExecution(ImmediateExecutionModel())
        
        # Use EqualWeightingPortfolioConstructionModel for portfolio construction 
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        
        # Set up risk management with a maximum drawdown of 5% per security 
        max_drawdown_pct = 5.0
        risk_model = MaximumDrawdownPercentPerSecurity(max_drawdown_pct)
        
        # Set up null risk management model (no stop loss or take profit orders) 
        null_risk_model = NullRiskManagementModel()
        
    def OnData(self,data):
        
         for symbol in data.Keys:
            
            if not data.Bars.ContainsKey(symbol):
                continue
                
            bar = data.Bars[symbol]
            
            # Get the security's TRIX indicator values from its data dictionary 
            trix_indicator_value = bar.SymbolData.Trix.Current.Value 
            trix_signal_indicator_value = bar.SymbolData.TrixSignal.Current.Value
            
            holdings_qty = int(self.Portfolio[symbol].Quantity)
            
             # Check if there is an open position and exit if opposite signal or trailing stop is hit             
             if holdings_qty > 0:
                exit_price_pct_change_threshold = -0.01   ## trail stop loss at -1% from entry price 
                exit_price_threshold_value = (1 + exit_price_pct_change_threshold) * entry_price
                
                if trix_signal_indicator_value < trix_indicator_value and bar.Close < exit_price_threshold_value:
                    order_ticket=self.Liquidate(symbol)  
                    continue
                
             elif holdings_qty < 0:
                exit_price_pct_change_threshold=-0.01   
                exit_price_threshold_value=(1-exit_price_pct_change_threshold)*entry_price
                
                if trix_signal_indicator_value > trix_indicator_value and bar.Close > exit_price_threshold_value:
                    order_ticket=self.Liquidate(symbol)  
                    continue
                    
             # Check if there is a signal to enter a new position             
             if trix_signal_indicator_value > trix_indicator_value and not holdings_qty:                 
                 atr_period=14   ## use ATR with period of 14 days                 
                 atr=self.ATR(bar.SymbolData.Symbol,'14')[-1]                 
                 stop_loss=bar.Close-(atr*1)   ## use ATR multiple of 1 as stop loss                 
                 entry_order_ticket=self.MarketOrder(bar.SymbolData.Symbol,-100)                 
                 entry_order_status=entry_order_ticket.Status                 
                 entry_order_filled=entry_order_ticket.QuantityFilled                
                 entry_order_avgFillPrice=entry_order_ticket.AverageFillPrice                
                
                  ## Wait until market order is filled before setting new stop-loss limit order               
                  while not entry_order_filled:                     
                     pass                
                  stop_limit_buy=self.StopMarketOrder(bar.SymbolData.Symbol,-100 ,stop_loss )                
                
    def OnOrderEvent(self,orderEvent):         
          order=self.Transactions.GetOrderById(orderEvent.OrderId)         
          if