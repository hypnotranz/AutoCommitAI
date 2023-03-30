

# Strategy_Volatility.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import AverageTrueRange
from datetime import timedelta

class Volatility(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)
        
        # Set symbol and add daily data
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Create Average True Range indicator
        self.atr = self.ATR(self.symbol, 14, MovingAverageType.Simple, Resolution.Daily)
        
        # Define trailing stop loss variables
        self.trailingStop = None
        self.trailingStopPercent = 0.02
        
    def OnData(self, data: TradeBar):
        
        # Do nothing until we have ATR data
        if not self.atr.IsReady:
            return
        
        # Check for trailing stop loss first
        if self.trailingStop is not None and data.Close < self.trailingStop:
            self.Liquidate()
            return
        
        # Calculate stop loss based on ATR and entry price
        stopPrice = data.Close - (2 * self.atr.Current.Value)
        
        # Check for exit signal (opposite signal or trailing stop)
#         if [exit criteria]:
#             [exit action]
        
    def OnOrderEvent(self, orderEvent):
        
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        
#         if [entry criteria]:
#             [entry action]
            
            # Set up trailing stop loss after entry
            entryPrice = order.AverageFillPrice
            trailPrice = entryPrice * (1 - self.trailingStopPercent)
            if not orderEvent.IsFill:
                return
            
            if orderEvent.Status == OrderStatus.Filled:
                if not self.Portfolio.Invested:
                    quantity = int(self.Portfolio.Cash / entryPrice)
                    marketOrder = MarketOrder(self.symbol, quantity)
                    trailStopOrder = StopMarketOrder(trailPrice, -quantity, "Trailing Stop Loss")
                    orderIdList = [marketOrder.Id, trailStopOrder.Id]
                    submitResponseList = list(map(lambda x: x.Value.SubmitRequest(), orderIdList))
                    submitResponseList.wait_all()
                    
                    marketFilledTimeUtcList = list(map(lambda x: x.Value.Time.UtcTime, marketOrder.OrderEvents))
                    filledTimeUtcIndexDict= {marketFilledTimeUtcList[i]: i for i in range(len(marketFilledTimeUtcList))}
                    
                    # Check to see which came first - the market or the trailing stop order fill.
                    trailFilledIndex= None
                    while trailFilledIndex is None:
                        for index in range(len(trailStopOrder.OrderEvents)):
                            fillTime= trailStopOrder.OrderEvents[index].FillTime.UtcTime.replace(microsecond=0,tzinfo=None)                        
                            if fillTime in filledTimeUtcIndexDict.keys():
                                trailFilledIndex= index + filledTimeUtcIndexDict[fillTime]
                                break
                        
                        time.sleep(1)                    
                    
                    
                    marketQuantityFilled= sum([marketOrder.OrderEvents[i].FillQuantity for i in range(filledTimeUtcIndexDict[marketFilledTimeUtcList[trailFilledIndex]])])
                    
                    remainingMarketQuantityToBeCanceled= quantity- marketQuantityFilled
                    
                    
                        
    
        
        
        
        
        
        
        
        

        
        
        
                
        
        
        
        
        
        
        
        
        
        

        
    
        


            
        
        
        
        

    
        
    
        
        
    
        
        
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    

    

    

    

    

    

    

    

    

    

    


    
    
    


    


    


    


    


    


    


    


    
        


            
        
        
        
        

    
        
    
        
        
    
        
        
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    




    
    
    
    
    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    

    

    

    

    

    

    

    

    

    

    
