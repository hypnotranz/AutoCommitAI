

# Strategy_Volume.py

from System import *
from QuantConnect import *
from QuantConnect.Data import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Orders import *

class Volume(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.atr = self.ATR(self.symbol, 14, MovingAverageType.Simple, Resolution.Daily)
        self.pvt = self.PVT(self.symbol)
        self.signal = Signal(self.pvt)
        
    def OnData(self, data):
        
        if not (self.pvt.IsReady and data.ContainsKey(self.symbol)):
            return
        
        if not self.Portfolio.Invested and self.signal.Current.Value > 0:
            limitPrice = data[self.symbol].Close
            stopPrice = data[self.symbol].Close - (self.atr.Current.Value * 1)
            quantity = int(self.Portfolio.Cash / limitPrice)
            orderTicket = self.LimitOrder(self.symbol, quantity, limitPrice)
            orderTicket.Update(new UpdateOrderFields { StopPrice=stopPrice })
            
        elif self.Portfolio.Invested:
            if (self.signal.Current.Value < 0) or (data[self.symbol].Close < orderTicket.StopPrice):
                self.Liquidate()
                
class Signal(IndicatorBase[IndicatorDataPoint]):
    
    def __init__(self, pvt):
        name = "Signal"
        pvt.Updated += lambda x: self.Update(x.Time, pvt.Current.Value)
        
    def Update(self, time: DateTime, value: Decimal):
        diff = value - pvt.Current.Value
        roc = diff / pvt.Current.Value * 100
        if roc > 0:
            return IndicatorDataPoint(time, +1)
        elif roc < 0:
            return IndicatorDataPoint(time, -1)
        else:
            return IndicatorDataPoint(time, 0)