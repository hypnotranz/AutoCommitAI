

# Volume_Strategy.py

from QuantConnect.Data import SubscriptionDataSource
from QuantConnect.Python import PythonData
from QuantConnect.Indicators import VolumePriceTrend
from datetime import timedelta


class Volume(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)

        # Add VPT indicator
        self.symbol = self.AddEquity("AAPL", Resolution.Daily).Symbol
        self.vpt = self.VPT(self.symbol, 14)

        # Set up entry and exit criteria
        self.signal = 0
        self.previous_signal = 0

        # Set up stop criteria
        self.atr = AverageTrueRange(14)
        self.stop_price = None

    def OnData(self, data):
        
        # Check for new VPT value
        if not self.vpt.IsReady:
            return

        # Update stop price with new ATR value
        if not self.stop_price:
            previous_close = data[self.symbol].Close - data[self.symbol].CloseDelta
            previous_high = data[self.symbol].High - data[self.symbol].HighDelta
            previous_low = data[self.symbol].Low - data[self.symbol].LowDelta
            
            true_range = max(previous_high - previous_low,
                             abs(previous_high - previous_close),
                             abs(previous_low - previous_close))
            
            self.stop_price = data[self.symbol].Close - true_range

        
        # Check for signal line cross
        if self.vpt.Signal.Current.Value > 0 and \
           self.vpt.Signal.Current.Value > self.vpt.Signal.Current.Value:
            if not (self.previous_signal < 0 and \
                    self.signal > 0):
                # Buy signal
                stop_loss_price = min(self.stop_price,
                                      data[self.symbol].Low + (self.atr.Current.Value * 1))
                quantity = int(self.CalculateOrderQuantity(self.symbol,
                                                           .05))
                orderTicket = None
                
                if not Portfolio.Invested:
                    orderTicket = \
                        self.MarketOrder(self.symbol,
                                         quantity,
                                         "Entry Long")
                    orderTicket.Update(new StopMarketOrderTicketParameters(stop_loss_price))
                    
                    if orderTicket.Status == OrderStatus.Filled:
                        pass
                    
                
                else:
                    orderTicket.Update(new StopMarketOrderTicketParameters(stop_loss_price))

                
                # Update signals and stop price
                if orderTicket.Status == OrderStatus.Filled:
                    fill_price = orderTicket.AverageFillPrice
                    
                    entry_stop_loss_distance_in_dollars_away_from_entry_point=(entry_stop_loss_distance_in_percentage_away_from_entry_point*fill_price)/100
                    
                    entry_take_profit_distance_in_dollars_away_from_entry_point=(entry_take_profit_distance_in_percentage_away_from_entry_point*fill_price)/100
                    
                    
                    take_profit_target=fill_price+entry_take_profit_distance_in_dollars_away_from_entry_point
                    
                    stop_loss_target=fill_price-entry_stop_loss_distance_in_dollars_away_from_entry_point
                    
                
                    quantity2=int((take_profit_target-stop_loss_target)/entry_stop_loss_distance_in_dollars_away_from_entry_point)
                    
                    
                    
                
                    

                
            

            
            


            
                
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                
                
                


        
        



    def OnEndOfDay(self):
        
#         history_vpt=History([self.Symbol("AAPL")], 
#                                      timedelta(days=14),
#                                      Resolution.Daily)
        
        
        
        
        
        
        
        

        

    def OnOrderEvent(self, orderEvent):
        
        

    def OnEndOfAlgorithm(self):
        
        
        
        

    def VPT(self, symbol, period):
        
        

    

    
    

    
    
    

    
        


    

            

            

            
            


            





                





    





        

    




        

        




    





    
                    

                    

                    


                

                

                

                

                

                

            

            
            
            




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




    
    
    
    
    




    
    
    
    
    
    
    


    
    

    
    
    
    
    
    


    
    

    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





   

            

            

            
            
            


                





    





        

    




        

        




    





    
                    

                    

                    


                

                

                

                

                

                

            

            
            
            




    
    
    
    
    


    
    

    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

  
    
  
    
    

  
    
  

  

  

  

  

  

  

  
  



  
  


  
  


  









      
      








  








        
        
        
        
        
        
        
        
        
        
        
        
        












        
        
        
        
       
     
  









      
      








  








        
        
        
        
        
        
        
        
        
        
        
        
        












        
        
        
        
       
     
  









      
      








  








        
        
        
        
        
        
        
        
        
        
        
        
        












        
        
        
        
       
     
  
        
    
        
    
        
    
        
    
        
    
        
    
        
            
              
            
              
            
              
            
              
            
              
             
            
              
            
             
 
         
     