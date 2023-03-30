

# Momentum_Strategy.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import Stochastic
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.Consolidators import TradeBarConsolidator
from QuantConnect.Orders.Fees import ConstantFeeModel
from System import *
import numpy as np


class Momentum(QCAlgorithm):

    def Initialize(self):
        
        self.SetStartDate(2010, 1, 1) 
        self.SetEndDate(2020, 1, 1)
        
        self.SetCash(100000) 
        
        # Equity universe selection
        equity = self.AddEquity("SPY", Resolution.Daily)
        
        # Add Stochastic indicator to the equity object
        self.stoch = self.STO("SPY", 14, 3, 3, Resolution.Daily)
        
        # Schedule the function every day for equity object to plot the indicator 
        self.Schedule.On(self.DateRules.EveryDay("SPY"), \
                          self.TimeRules.AfterMarketOpen("SPY", 0), \
                          Action(self.EquityDailyChart))
        
        # Set portfolio construction model to momentum portfolio construction model
        self.SetPortfolioConstruction(MomentumPortfolioConstructionModel())
        
        # Set execution model to Immediate Execution Model
        self.SetExecution(ImmediateExecutionModel())
        
        # Set Risk Management Model to Trailing Stop Model
        self.SetRiskManagement(TrailingStopRiskManagementModel())


    def EquityDailyChart(self):
        
      # Plot the stochastic oscillator of the equity object daily using plot function
        
      if not self.stoch.IsReady:
          return
      
      plot = Chart('Stochastic Oscillator')
      plot.AddSeries(Series('Stoch', SeriesType.Line, 0))
      plot.AddSeries(Series('Overbought', SeriesType.HorizontalLine, high_threshold))
      plot.AddSeries(Series('Oversold', SeriesType.HorizontalLine, low_threshold))
      
      for time in [x.Time for x in self.stoch]:
          plot.Series['Stoch'].AddPoint(time, self.stoch.Current.Value)
      
      plot.Title = 'Stochastic Oscillator'
      
      if not self.Plot.ContainsKey(plot.Title):
          self.Plot.Add(plot)

class MomentumPortfolioConstructionModel:
    
    def __init__(self):
       
       pass
    
    def CreateTargets(self, algorithm: QCAlgorithm, insights: List[Insight]) -> List[PortfolioTarget]:
       
       targets = []
       
       for insight in insights:
           
           if insight.Direction == InsightDirection.Up:
               targets.append(PortfolioTarget(insight.Symbol, insight.Score))
           else:
               targets.append(PortfolioTarget(insight.Symbol, -insight.Score))
       
       return targets


class TrailingStopRiskManagementModel(RiskManagementModel):

    def __init__(self):
       
       pass
    
    def ManageRisk(self, algorithm: QCAlgorithm, direction: int) -> List[RiskManagementAction]:
      
       actions = []
       
       holdings = algorithm.Portfolio[algorithm.Symbol].Quantity
      
       if holdings == 0:
           return actions
      
       open_orders = algorithm.Transactions.GetOpenOrders(algorithm.Symbol)
       
       if len(open_orders) > 0:
           return actions
      
       atr = algorithm.ATR(algorithm.Symbol.Value ,14)
    
       if direction == RiskManagementDirection.Long:
           
           stop_price = algorithm.Securities[algorithm.Symbol].Price - atr.Current.Value

           actions.append(RiskManagementAction(algorithm.Symbol,RiskManagementActionType.StopMarket ,direction,\
                                                holdings,-stop_price,'Trailing Stop Loss'))
           
           
           
          
           
                   
           
          
           
                 
           
                     
           
               
              
                          
                          
                          
                          
                          
                          
                          
          
                                    
                                    
                                    
                                                                                                         
     
     
     
     
     
                   
                                            
                                                
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
    
                                                         
    
                                                         
    
                                                         
    
                                                         
     
                                                             
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    
    

class ImmediateExecutionModel(ExecutionModel):

    def __init__(self):
       
       pass
    
    def Execute(self, algorithm: QCAlgorithm,packet:OrderTicket) -> None:
       
          pass
        
        
        
        
        
        
    
        
        
        
        
        
        
        
    
    
 

    





   
    
    
        
        
    
        

        

    

        

    

        
    
        

    





       

        
    
        
        
        

        

        



        
    
        


        
    
        


    
    
    
    



    
    
    
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
            
             
                 
                     
                         
                             
                                 
                                     
                                         
    

      

    

      

      
        

      
        
    
            
            
            
            
            
            
            
            
            
            

            
            

            
            
            
            
            





         
                
                    
                    
                    
                    
                    
                        
                            
                                
                                    
                                        
                                            
                                                
                                                    
                                                        
                                                            
                                                                 
                                                                     
                                                                         
                                                                             
                                                                                 
    
                    
                        
                            
                                
                                    
                                        
                                            
                                                
                                                    
                                                        
                                                            
                                                                 
                                                                     
                                                                         
                                                                             
                                                                                 
    
                
                    
                    
                    
                    
                    
                        
                            
                                
