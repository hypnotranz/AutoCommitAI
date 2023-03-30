

# Trend Following with Parabolic SAR
from QuantConnect.Indicators import ParabolicStopAndReverse
from QuantConnect.Data.Market import TradeBar

class TrendFollowingParabolicSAR(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)

        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Set up Parabolic SAR indicator with default settings
        self.psar = self.PSAR(self.symbol)

        # Set up ATR indicator with period of 14
        self.atr = self.ATR(self.symbol, 14)

        # Set up trailing stop value as 1 x ATR
        self.trailingStopValue = None

    def OnData(self, data: TradeBar):
        
        if not self.psar.IsReady:
            return

        # Check for long entry signal: price above dots
        if data.Close > self.psar.Current.Value and data.Close > self.psar.SAR.Current.Value:
            if not self.Portfolio.Invested:
                # Calculate number of shares to buy based on risk percentage (2% here)
                riskPercent = 0.02
                stopPrice = data.Close - (self.atr.Current.Value * riskPercent)
                sharesToBuy = int(self.Portfolio.Cash / (data.Close - stopPrice))
                
                # Buy shares and set trailing stop value
                orderTicket = self.MarketOrder(self.symbol, sharesToBuy)
                if orderTicket.Status == OrderStatus.Filled:
                    order = orderTicket.Order
                    stopMarketOrderTicket = self.StopMarketOrder(self.symbol, -order.AbsoluteQuantity, stopPrice)
                    if stopMarketOrderTicket.Status == OrderStatus.Submitted:
                        stopMarketOrder = stopMarketOrderTicket.Order
                        self.trailingStopValue = stopMarketOrder.StopPrice + (self.atr.Current.Value * riskPercent)

        # Check for short entry signal: price below dots
        elif data.Close < self.psar.Current.Value and data.Close < self.psar.SAR.Current.Value:
            if not self.Portfolio.Invested:
                # Calculate number of shares to sell short based on risk percentage (2% here)
                riskPercent = 0.02
                stopPrice = data.Close + (self.atr.Current.Value * riskPercent)
                sharesToSellShort = int(self.Portfolio.Cash / (stopPrice - data.Close))

                # Sell short and set trailing stop value
                orderTicket = self.MarketOrder(self.symbol, -sharesToSellShort)
                if orderTicket.Status == OrderStatus.Filled:
                    order = orderTicket.Order
                    stopMarketOrderTicket = StopMarketOrder(self.symbol, -order.AbsoluteQuantity, stopPrice)
                    if stopMarketOrderTicket.Status == OrderStatus.Submitted:
                        stopMarketOrder = stopMarketOrderTicket.Order
                        trailingStopValue=stopMarketOrder.StopPrice - (self.atr.Current.Value * riskPercent)

        # Check for exit signal: opposite signal or trailing stop hit
        elif (data.Close < psar.SAR.Current.Value and psar.IsRising) or \
            (data.Close > psar.SAR.Current.Value and psar.IsFalling) or \
            (self.trailingStopValue is not None and 
             ((self.Portfolio.Invested and data.Low < trailingStopValue) or 
              ((not Portfolio.Invested) and data.High > trailingStopValue))):
            
            if Portfolio.Invested:
              # Liquidate holdings on exit signal 
              liquidateReturns=self.Liquidate()
              for r in liquidateReturns:
                  pass
            
            # Reset trailingStopValue to None on exit signal 
            trailingStopValue=None