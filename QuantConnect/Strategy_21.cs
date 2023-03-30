

# Momentum_Trix_Signal_TrailingStop.py

from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import Trix
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.Consolidators import TradeBarConsolidator
from QuantConnect.Orders import OrderStatus, OrderType, TimeInForce


class Momentum(QCAlgorithm):

    def Initialize(self):
        '''Initialise the algorithm'''

        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2016, 1, 1)
        self.SetCash(100000)

        # Add the asset to trade and set the custom data
        self.symbol = self.AddEquity("AAPL", Resolution.Daily).Symbol

        # Create a trix indicator
        trix = self.TRIX(self.symbol, 30)

        # Create a consolidator to trigger the trix indicator every day
        consolidator = TradeBarConsolidator(timedelta(1))
        consolidator.DataConsolidated += lambda sender, consolidated: trix.Update(consolidated.Time, consolidated.Close)

        # Register the consolidator to receive data from the asset
        self.SubscriptionManager.AddConsolidator(self.symbol, consolidator)

    def OnData(self, data):
        
            # Determine whether we have a position open or not.
            holdings = sum([x.Quantity for x in self.Portfolio if x.Invested])

            # Get the latest TRIX value.
            trix = self.Securities[self.symbol].Indicator[Trix](30)
            trix_value = trix.Current.Value

            if holdings == 0:
                # Check for a TRIX signal line cross.
                if trix.IsReady and trix.Current.Value > trix.Signal.Current.Value:
                    # Buy using a market order.
                    quantity = int(self.Portfolio.Cash / data[self.symbol].Close)
                    self.MarketOrder(self.symbol, quantity)

                    # Set stop loss order.
                    stop_price = data[self.symbol].Close - (self.ATR(self.symbol, 14).Current.Value * 1)
                    stop_loss_order_ticket = self.StopMarketOrder(self.symbol, -quantity,
                                                                  stop_price)
            else:
                if trix.IsReady:
                    if (trix.Current.Value < trix.Signal.Current.Value) or (data[self.symbol].Close < stop_price):
                        order_ticket = None
                        for ticket in self.Transactions.GetOpenOrders():
                            if ticket.Symbol == self.symbol:
                                order_ticket = ticket

                        if order_ticket is not None and order_ticket.Status != OrderStatus.Filled:
                            continue

                        sell_quantity = holdings if holdings > 0 else -holdings
                        order_ticket = self.MarketOrder(self.symbol, -sell_quantity)

                        if order_ticket.Status == OrderStatus.Filled:
                            stop_loss_order_ticket.Cancel()