

# Momentum.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import ChandeMomentumOscillator
from QuantConnect.Algorithm.Framework import QCAlgorithmFramework
from QuantConnect.Algorithm.Framework.Selection import ManualUniverseSelectionModel


class Momentum(QCAlgorithmFramework):
    
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        
        self.UniverseSettings.Resolution = Resolution.Daily
        
        self.AddUniverse(self.CoarseSelectionFunction)
        
        self.cmo = {}
        for symbol in self.symbols:
            self.cmo[symbol] = ChandeMomentumOscillator(symbol, 14)
        
    def CoarseSelectionFunction(self, coarse):
        sortedByDollarVolume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:50]
        symbols = [x.Symbol for x in sortedByDollarVolume]
        return symbols
    
    def OnSecuritiesChanged(self, changes):
        
        for security in changes.AddedSecurities:
            symbol = security.Symbol
            if not security.HasData:
                continue
                
            cmo_indicator = self.cmo[symbol]
            self.RegisterIndicator(symbol, cmo_indicator, Resolution.Daily)
            
    def OnData(self, data):
        
        if not all([cmo.IsReady for cmo in self.cmo.values()]):
            return
        
        holdings = {x.Key:x.Value.Quantity for x in self.Portfolio}
        
        for symbol in holdings:
            
            # Exit criteria: opposite signal or trailing stop
            if holdings[symbol] > 0 and ((self.cmo[symbol].Current.Value < 0 and not symbol in data.GetLastKnownPrice()) or (symbol in data.GetLastKnownPrice() and holdings[symbol] * (data.GetLastKnownPrice()[symbol].High - data.GetLastKnownPrice()[symbol].Close) < -self.atr[symbol])):
                self.Liquidate(symbol)
                
            # Entry criteria: crossing zero line
            elif holdings[symbol] == 0 and (self.cmo[symbol].Current.Value > 0 and not symbol in data.GetLastKnownPrice()):
                limit_price = data.GetLastKnownPrice()[symbol].Close * 1.01
                stop_price = data.GetLastKnownPrice()[symbol].Close - (self.atr[symbol] * 1)
                qty = int(self.Portfolio.Cash / limit_price)
                if qty > 0:
                    self.MarketOrder(symbol, qty)