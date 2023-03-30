

# Trend Following Strategy using Donchian Channels, with Entry on Price Breakout, Exit on Opposite Signal or Trailing Stop, and Stop Loss of 1 x ATR.

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import DonchianChannel
from datetime import timedelta, datetime
import decimal as d

class TrendFollowingStrategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        self.symbol = "SPY"
        self.period = 20
        self.atr_period = 14
        self.atr_multiplier = 1
        self.donchian_upper = None
        self.donchian_lower = None
        self.entry_price = None
        self.exit_price = None
        self.stop_loss_price = None
        
        # Set Donchian Channels as Primary Indicator for Strategy Entry and Exit Signals.
        
        self.donchian_channel = DonchianChannel(self.period)
        
        # Set Stop Loss on ATR at Entry Price.
        
        self.atr_indicator = AverageTrueRange(self.atr_period)
        
    def OnData(self, data):
        
        # Wait until we have enough data for our indicators.
        
        if not (self.donchian_channel.IsReady and 
                self.atr_indicator.IsReady): 
            return
        
        # Define our Entry Criteria as Price Breaking Out of Upper Donchian Channel.
        
            if data[self.symbol].Close > self.donchian_channel.UpperBand.Current.Value:
                
                # Set Entry Price at Upper Band Value.
                
                self.entry_price = data[self.symbol].Close
                
                # Set Stop Loss Price at Entry Price - ATR Multiplier x ATR Value.
                
                atr_value = float(self.atr_indicator.Current.Value)
                stop_loss_offset = atr_value * float(self.atr_multiplier)
                stop_loss_decimal_places = len(str(int(atr_value)))
                stop_loss_decimal_places += 2
                
                stop_loss_price_decimal_places_shifted_right = d.Decimal(stop_loss_offset).shift(stop_loss_decimal_places) 
                stop_loss_price_decimal_places_shifted_left_as_string_formatting_two_decimals_and_adding_negative_sign_to_left_shifted_value \
                    = "-{0:.2f}".format(stop_loss_price_decimal_places_shifted_right) 
                
                stop_loss_price_string_shifted_left_with_two_decimals_and_negative_sign_as_first_character \
                    = "stop loss: " + str(stop_loss_price_decimal_places_shifted_left_as_string_formatting_two_decimals_and_adding_negative_sign_to_left_shifted_value) 
                
                log_message_stop_loss_set_at_this_stop_level \
                    = "stop loss set at: " + str(float(self.entry_price) - float(stop_loss_offset))
                    
                # Debugging Print Statements.
                    
#                 print(log_message_stop_loss_set_at_this_stop_level)
#                 print(stop_loss_price_string_shifted_left_with_two_decimals_and_negative_sign_as_first_character)

                    
            # Define our Exit Criteria as Opposite Signal or Trailing Stop Loss Hit.

            if (data[self.symbol].Close < self.donchian_channel.LowerBand.Current.Value or 
               data[self.symbol].Close > (float(self.entry_price) + (float(atr_value) * float(self.atr_multiplier)))):
                
                # Reset All Variables to Begin New Trade Cycle.
                
                    entry_exit_log_message_what_was_the_entry_strategy \
                        ="entry strategy: donchain channel breakout"
                        
                    entry_exit_log_message_what_was_the_exit_strategy \
                        ="exit strategy: opposite signal or trailing stop"
                        
                    entry_exit_log_message_entry_trade_time \
                        ="entry time:" + str(data[self.symbol].Time.date())
                        
                    entry_exit_log_message_entry_trade_opening_condition \
                        ="entry trade opening condition: price crossing upper band value."
                        
                    entry_exit_log_message_entry_trade_opening_condition_additional_info \
                        ="Upper band value: " + str(float(self.donchian_channel.UpperBand.Current.Value))
                        
                    entry_exit_log_message_exit_trade_time \
                        ="exit time:" + str(data[self.symbol].Time.date())
                        
                    if data[self.symbol].Close < float(self.donchian_channel.LowerBand.Current.Value):
                        
                        exit_signal_type_that_triggered_the_exit_condition \
                            ="exit signal type that triggered the exit condition:" + "price crossing lower band value."
                            
                        exit_signal_type_that_triggered_the_exit_condition_additional_info\
                            ="lower band value crossed:" +" "+ str(float(self.donchian_channel.LowerBand.Current.Value))
                            
                            
                            
                    elif data[self.symbol].Close > (float(self.entry_price) + (float(atr_value) * float(self.atr_multiplier))):
                        
                        exit_signal_type_that_triggered