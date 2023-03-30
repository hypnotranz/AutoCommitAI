

# Strategy_RangeTrading.py

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar

class RangeTrading(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  
        self.SetEndDate(2019, 12, 31) 
        self.SetCash(100000)  
        
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.upperEnvelopes = self.EMA(self.symbol, 20, 0.05)
        self.lowerEnvelopes = self.EMA(self.symbol, 20, -0.05)
        
        self.atr = self.ATR(self.symbol, 14)
        
        self.tradingOpened = False
        
        # set the Envelopes as plot
        upperChart = Chart('Upper Envelopes')
        upperChart.AddSeries(Series('Upper', SeriesType.Line, 0))
        upperChart.AddSeries(Series('Price', SeriesType.Line, 1))
        
        lowerChart = Chart('Lower Envelopes')
        lowerChart.AddSeries(Series('Lower', SeriesType.Line, 0))
        lowerChart.AddSeries(Series('Price', SeriesType.Line, 1))
        
        atrChart = Chart('ATR')
        atrChart.AddSeries(Series('ATR', SeriesType.Line, 0))
        
        # add the charts to the algorithm
        self.AddChart(upperChart)
        self.AddChart(lowerChart)
        self.AddChart(atrChart)
        
    def OnData(self,data):
       
       if not (self.upperEnvelopes.IsReady and
               self.lowerEnvelopes.IsReady and
               data.ContainsKey(self.symbol)): 
           return 
        
       closePrice = data[self.symbol].Close
        
       # plot the upper and lower envelopes and price
       upperValue = float(self.upperEnvelopes.Current.Value)
       lowerValue = float(self.lowerEnvelopes.Current.Value)
       atrValue = float(self.atr.Current.Value)

       # update the charts with the new value
       upperDataPoint = ChartDataPoint(data[self.symbol].EndTime,
                                        upperValue)
                                        
       priceDataPoint = ChartDataPoint(data[self.symbol].EndTime,
                                        closePrice)

       lowerDataPoint=ChartDataPoint(data[self.symbol].EndTime,
                                      lowerValue)

       atrDataPoint=ChartDataPoint(data[self.symbol].EndTime,
                                    atrValue)

       chartNames=['Upper Envelopes','Lower Envelopes','ATR']

       for chart in chartNames:
           if chart == 'Upper Envelopes':
               self.Plot(chart,'Upper',upperDataPoint)
               self.Plot(chart,'Price',priceDataPoint)

           elif chart == 'Lower Envelopes':
               self.Plot(chart,'Lower',lowerDataPoint)   
               self.Plot(chart,'Price',priceDataPoint)

           elif chart == 'ATR':
               	self.Plot(chart,'ATR',atrDataPoint)        
        
       
      if not (self.upperEnvelopes.IsReady and
              data.ContainsKey(self.symbol)): 
           return

      if not (self.lowerEnvelopes.IsReady and 
              data.ContainsKey(self.symbol)): 
          return
        
      if not (self.atr.IsReady and 
              data.ContainsKey(self.symbol)): 
          return
        
      position=self.Portfolio[self.symbol].Quantity
      
      if not position: # no position open yet
      
          if closePrice>upperValue:
              stopPrice=closePrice-0.5*atrValue
              takeProfit=closePrice-atrValue
              stopMarketTicket=self.StopMarketOrder(
                  symbol=self.Symbol,
                  quantity=self.CalculateOrderQuantity(symbol=self.Symbol),
                  stopPrice=stopPrice,
                  tag='Stop Loss')

              takeProfitTicket=self.LimitOrder(
                  symbol=self.Symbol,
                  quantity=-self.CalculateOrderQuantity(symbol=self.Symbol),
                  limitPrice=takeProfit,
                  tag='Take Profit')

              orderTicket=self.MarketOrder(
                  symbol=self.Symbol,
                  quantity=self.CalculateOrderQuantity(symbol=self.Symbol),
                  tag='Entry Order')

              # record order tickets in order to track them later
              orderTicket.Tag='Entry Order'
              takeProfitTicket.Tag='Take Profit'
              stopMarketTicket.Tag='Stop Loss'
              
              
          elif closePrice<lowerValue:
              
                stopPrice=closePrice+0.5*atrValue
                takeProfit=closePrice+atrValue
                
                stopMarketTicket=self.StopMarketOrder(
                    symbol=self.Symbol,
                    quantity=-self.CalculateOrderQuantity(symbol=self.Symbol),
                    stopPrice=stopPrice,
                    tag='Stop Loss')

                takeProfitTicket=self.LimitOrder(
                    symbol=self.Symbol,
                    quantity=-self.CalculateOrderQuantity