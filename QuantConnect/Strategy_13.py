

# Volume.py

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import *
from QuantConnect.Orders import *

class Volume(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2015,1,1)
        self.SetEndDate(2019,1,1)
        self.SetCash(100000)
        self.AddEquity("AAPL", Resolution.Daily)
        self.slowEMAKVO = self.EMA("AAPL", 34)
        self.fastEMAKVO = self.EMA("AAPL", 15)
        self.KVO = KlingerVolumeOscillator(self.slowEMAKVO, self.fastEMAKVO, 34, 55, 13)
        
    def OnData(self,data):
        
        if not (self.slowEMAKVO.IsReady and self.fastEMAKVO.IsReady and 
                self.KVO.Signal.IsReady and self.KVO.IsReady): return
        
        if not self.Portfolio.Invested:
            if (self.KVO.Signal.Current.Value > 0):
                stopPrice = data["AAPL"].Low * 0.985
                limitPrice = data["AAPL"].Close * 1.02
                quantity = int(self.Portfolio.Cash / data["AAPL"].Close)
                if quantity == 0: return
                ticket = self.LimitOrder("AAPL", quantity, limitPrice)
                stopMarketTicket =self.StopMarketOrder("AAPL", -quantity, stopPrice)  
            
            return
        
        else:
            if (self.KVO.Signal.Current.Value < 0):
                quantity = int(self.Portfolio["AAPL"].Quantity * -1)  
                stopPrice = data["AAPL"].High * 1.015
                stopMarketTicket=self.StopMarketOrder("AAPL", quantity, stopPrice) 
                
            return
        
            # Define trailing stop loss
            holdings = list(self.Portfolio.Values)
            for holding in holdings:
                symbol = holding.Symbol
                atrValue = str(round(self.ATR(symbol).Current.Value*1.5 ,2))
                if holding.Invested and symbol == "AAPL":
                    for order in holding.Orders:
                        if order.Type == OrderType.StopMarket and order.Quantity > 0:
                            newStopPrice = float(order.StopPrice) + float(atrValue)
                            updateFields=UpdateOrderFields()
                            updateFields.StopPrice= newStopPrice
                            ticket=self.UpdateOrder(order.Id, updateFields)