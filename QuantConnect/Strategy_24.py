

# Strategy_TrendFollowing.py

from QuantConnect.Data.Custom import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Orders import *


class TrendFollowing(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)

        # Universe selection
        symbols = [Symbol.Create("SPY", SecurityType.Equity, Market.USA)]
        self.UniverseSettings.Resolution = Resolution.Daily

        self.AddUniverseSelection(ManualUniverseSelectionModel(symbols))
        self.UniverseSettings.DataNormalizationMode = DataNormalizationMode.Raw

        # Trading settings
        self.entry_price = {}
        self.exit_price = {}
        self.stop_price = {}
        self.trailing_stop_pct = 0.005
        self.atr_period = 14
        self.atr_multiplier = 2

    def OnData(self, data):

        for symbol in data.Keys:
            if symbol not in self.entry_price:
                # Initialize indicators for new symbols
                zigzag = ZigZagHighLow(symbol, percentage=5)
                atr = AverageTrueRange(self.atr_period)

                # Store indicators and current prices in dictionaries
                self.entry_price[symbol] = None
                self.exit_price[symbol] = None
                self.stop_price[symbol] = None
                setattr(self, f"{symbol}_zigzag", zigzag)
                setattr(self, f"{symbol}_atr", atr)

            # Update indicators and prices for existing symbols
            zigzag_indicator = getattr(self, f"{symbol}_zigzag")
            atr_indicator = getattr(self, f"{symbol}_atr")

            current_price_data = data.Get(symbol)
            current_high_low_data_point: IndicatorDataPointHighLowExtended \
                 = IndicatorDataPointHighLowExtended.FromData(
                     current_price_data,
                     current_price_data.High,
                     current_price_data.Low,
                     current_price_data.Volume,
                     None,
                 )

            zigzag_indicator.Update(current_high_low_data_point)

            if not zigzag_indicator.IsReady:
                continue

            high_low_extremum: IndicatorDataPointHighLowExtended \
                 = zigzag_indicator.Current.Value

            # Exit if opposite signal or trailing stop triggered
            if (
                    (self.entry_price[symbol] is not None) and (
                        (current_high_low_data_point.Low <
                         (1 - self.trailing_stop_pct) * max(
                             high_low_extremum.High,
                             high_low_extremum.Low,
                             )
                         ) or (
                            (self.exit_price[symbol] is not None) and (
                                ((self.exit_price[symbol].Direction ==
                                  OrderDirection.Buy) and (
                                      high_low_extremum.High <
                                      max(zigzag_indicator.ZigZag.Current.Value.High,
                                          zigzag_indicator.ZigZag.Current.Value.Low))
                                 ) or (
                                    (self.exit_price[symbol].Direction ==
                                     OrderDirection.Sell) and (
                                         high_low_extremum.Low >
                                         min(zigzag_indicator.ZigZag.Current.Value.High,
                                             zigzag_indicator.ZigZag.Current.Value.Low))
                                    )
                                )
                            )
                        )
                    ):
                    
                    order_ticket: OrderTicket \
                         = Transactions.GetOrderTickets(self.exit_price[symbol].OrderId)[0]

                    if order_ticket.Status != OrderStatus.Filled:
                        continue

                    if order_ticket.Status == OrderStatus.Filled:
                        delattr(self, f"{symbol}_zigzag")
                        delattr(self, f"{symbol}_atr")
                        delattr(self.entry_price[symbol])
                        delattr(self.exit_price[symbol])
                        delattr(self.stop_order_id[symbol])
                        
                    continue

            # Enter long position if a new high has been reached since the last entry point with sufficient volatility 
            elif (current_high_low_data_point.High > high_low_extremum.High) \
                 and (current_high_low_data_point.Volume >= atr_indicator.Current.Value):
                
                stop_loss_pct: float \
                     = max(
                         ((high_low_extremum.High - current_high_low_data_point.Low)
                          /high_low_extremum.High),
                         ((high_low_extremum.High - current_high_low_data_point.Close)
                          /high_low_extremum.High),
                         ((high_low_extremum.High - current_high_low_data_point.Open)
                          /high_low_extremum.High),
                     ) * 100
                
                
                stop_loss_distance: float \
                     =(stop_loss_pct/100)*current_high_low_data_point.Close
                
                
                stop_order: StopMarketOrder \
                     =(StopMarketOrder(symbol,-1*stop_loss_distance))
                
                
                
                    
                        
                
                
                

                
                
                
                    
                        
                
                
                

                
                
                
                    
                        
                
                
                

