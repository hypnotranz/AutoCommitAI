

# Strategy_Volume.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import KlingerVolumeOscillator, ExponentialMovingAverage, AverageTrueRange
from datetime import timedelta


class Volume(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  
        self.SetEndDate(2021, 12, 31)  
        self.SetCash(100000)  
        self.symbol = self.AddEquity("AAPL", Resolution.Daily).Symbol  

        # Indicators
        self.kvo = KlingerVolumeOscillator(20)
        self.sma = ExponentialMovingAverage(10)
        self.atr = AverageTrueRange(14)

        # Signals
        self.buy_signal_triggered = False
        self.sell_signal_triggered = False

    def OnData(self, data: TradeBar):
        
        if not (self.kvo.IsReady and self.sma.IsReady and self.atr.IsReady):
            return
        
        kvo_value = round(self.kvo.Current.Value, 4)
        
        if not (self.buy_signal_triggered or self.sell_signal_triggered):
            if kvo_value > 0 and kvo_value > round(self.kvo.Signal.Current.Value, 4):
                # Buy Signal triggered
                stop_price = data.Close - (self.atr.Current.Value * 1.5)
                self.buy_order_ticket = self.MarketOrder(self.symbol, 1000, stop_price=stop_price)
                self.buy_signal_triggered = True
                
            elif kvo_value < 0 and kvo_value < round(self.kvo.Signal.Current.Value, 4):
                # Sell Signal triggered
                stop_price = data.Close + (self.atr.Current.Value * 1.5)
                self.sell_order_ticket = self.MarketOrder(self.symbol, -1000, stop_price=stop_price)
                self.sell_signal_triggered = True
                
            else:
                return
        
        elif not (self.Portfolio[self.symbol].Invested or 
                  (self.buy_order_ticket.Status == OrderStatus.Filled or 
                   abs(self.sell_order_ticket.QuantityFilled) == abs(self.sell_order_ticket.Quantity))):
            return
        
        else:
            # Exit Criteria Met
            if ((kvo_value < round(self.kvo.Signal.Current.Value, 4) and 
                 not abs(self.Portfolio[self.symbol].InvestedQuantity) == abs(int(self.sell_order_ticket.QuantityFilled))) 
                    or 
                    (kvo_value > round(self.kvo.Signal.Current.Value, 4) and 
                     not abs(int(self.buy_order_ticket.QuantityFilled)) == abs(int(self.buy_order_ticket.Quantity)))):
                
                if abs(int(self.Portfolio[self.symbol].InvestedQuantity)) == abs(int(self.buy_order_ticket.Quantity)):
                    # Exiting Long Position
                    sell_quantity = -1000 if int(abs(int((self.Portfolio[self.symbol].InvestedQuantity)))) >= 1000 else int(abs(int((self.Portfolio[self.symbol].InvestedQuantity))))
                    sell_stop_price = data.Close - (self.atr.Current.Value * 1.5)
                    sell_resulting_order_ticket = None
                    
                    while True:
                        sell_resulting_order_ticket = \
                            (self.stop_market_sell(sell_quantity,
                                                   sell_stop_price))
                        if sell_resulting_order_ticket is None:
                            continue

                        break
                    
                    # Reset Signals & Order Tickets
                    delattr(self,"buy_signal_triggered")
                    delattr(self,"sell_signal_triggered")
                    
                elif abs(int(self.Portfolio[self.symbol].InvestedQuantity)) == abs(int(abs((self.sell_order_ticket.QuantityFilled)))):
                    
                    buy_quantity=1000 if int(abs(int((self.Portfolio[self.symbol].InvestedQuantity)))) >=1000 else int(abs(int((self.Portfolio[self.symbol].InvestedQuantity))))
                    
                    buy_stop_price=data.Close + (self.atr.Current.Value * 1.5)
                    
                    while True:
                        buy_resulting_orderTicket=(self.stopMarketBuy(buy_quantity,buy_stop_price))
                        
                        if buy_resulting_orderTicket is None:
                            continue
                        
                        break
                        
                     # Reset Signals & Order Tickets   
                        
    def stop_market_sell(sell_quantity: int,
                             sell_stop_price: float,
                             maximum_attempts: int=20)-> Optional[OrderTicket]:
        
         for i in range(maximum_attempts):
             
             orderTicket=self.StopMarketOrder(
                 Symbol=self.Symbol,
                 Quantity=sell_quantity,
                 StopPrice=sell_stop_price)

             return orderTicket

         print("Maximum attempts reached for StopMarketSell")
         return None
    
    def stop_market_buy(buy_quantity: int,
                            buy_stopPrice: float,
                            maximum_attempts: int=20)-> Optional[OrderTicket]:
        
         for i in range(maximum_attempts):
             
             orderTicket=self.StopMarketOrder(
                 Symbol