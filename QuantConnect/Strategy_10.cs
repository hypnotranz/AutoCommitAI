

# Strategy_Momentum.py

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar


class Momentum(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        self.AddEquity("SPY", Resolution.Daily)

        self.cmo = CMO("SPY", 14, Resolution.Daily)
        self.atr = ATR("SPY", 14, MovingAverageType.Simple, Resolution.Daily)

        self.previous_cmo = None
        self.position_size = None
        self.stop_price = None

    def OnData(self, data: TradeBar):
        if not (self.cmo.IsReady and self.atr.IsReady):
            return

        # Long entry
        if self.cmo.Current.Value > 0 and (self.previous_cmo is None or self.previous_cmo <= 0):
            # Calculate position size based on risk
            risk_per_share = float(self.atr.Current.Value)
            target_risk_pct = 0.01
            target_price = data.Close + (target_risk_pct * risk_per_share)
            stop_price = data.Close - risk_per_share

            if stop_price < data.Low:
                return

            position_size_dollars = (self.Portfolio.TotalPortfolioValue * target_risk_pct) / (target_risk_pct * risk_per_share)

            # Ensure that the position size is not larger than the available cash
            position_size_dollars = min(position_size_dollars, self.Portfolio.Cash)

            # Convert dollars to shares
            position_size_shares = int(position_size_dollars / data.Close)

            # Place order
            self.SetHoldings("SPY", position_size_shares / 100)

            # Store values for exit and stop loss logic
            self.position_size = position_size_shares / 100
            self.stop_price = stop_price

        # Exit on opposite signal or trailing stop loss
        if ((self.position_size is not None) and (self.stop_price is not None)):
            if ((self.cmo.Current.Value < 0) and (self.previous_cmo > 0)) or (data.Close < self.stop_price):
                # Exit position
                if not self.Portfolio["SPY"].IsShort:
                    self.Liquidate("SPY")

                    # Reset values for next entry signal
                    self.position_size = None
                    self.stop_price = None

        # Update previous CMO value for next iteration
        self.previous_cmo = float(self.cmo.Current.Value)