# TrendFollowing_ADX.py

from datetime import timedelta
from typing import Type

from QuantConnect import QCAlgorithm
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import (
    AverageDirectionalIndex,
    AverageTrueRange,
    ExponentialMovingAverage,
    RelativeStrengthIndex,
)
from QuantConnect.Orders import OrderStatus, UpdateOrderFields


class TrendFollowingADX(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)

        # Add equity
        equity = self.AddEquity("SPY", Resolution.Daily)

        # Set up indicators
        self.adx = AverageDirectionalIndex(14)
        self.ema20 = ExponentialMovingAverage(20)
        self.rsi = RelativeStrengthIndex(14)
        self.atr = AverageTrueRange(14)

    def OnData(self, data: TradeBar):
        if not (
            self.adx.IsReady and self.ema20.IsReady and self.rsi.IsReady and self.atr.IsReady
        ):
            return

        # Check for entry criteria
        if not self.Portfolio.Invested and (
            self.adx.Current.Value > 20
        ) and (
            data.Close > self.ema20.Current.Value
        ) and (
            self.rsi.Current.Value > 50
        ):
            stopPrice = data.Close - 2 * self.atr.Current.Value
            quantity = int(self.Portfolio.Cash / data.Close)
            if quantity == 0:
                return

            # Place buy order with stop loss
            orderTicket = self.MarketOnCloseOrder("SPY", quantity, stopPrice)

            if orderTicket.Status != OrderStatus.Filled:
                return

            # Set trailing stop loss
            updateFields = UpdateOrderFields()
            updateFields.StopPrice = stopPrice * 0.95
            updateFields.Tag = "TrailingStopLoss"
            updateFields.Quantity = quantity
            updateFields.Symbol = "SPY"
            updateFields.OrderType = OrderType.StopMarket

            orderTicket.Update(updateFields)

        # Check for exit criteria
        elif self.Portfolio.Invested:

            holdingPeriodDays = (self.Time - self.Portfolio.InvestedTime).days

            if holdingPeriodDays >= 5:
                stopLossOrderTickets = [
                    x
                    for x in self.Transactions.GetOrderTickets()
                    if x.Symbol == "SPY"
                    and x.Status == OrderStatus.Submitted
                    and x.Tag == "TrailingStopLoss"
                ]

                if len(stopLossOrderTickets) > 0:
                    # Cancel previous trailing stop orders
                    for ticket in stopLossOrderTickets:
                        ticket.Cancel()

                if (
                    self.adx.Current.Value < 20
                ) or (
                    (data.Close < self.ema20.Current.Value)
                    and (self.rsi.Current.Value < 50)
                ):
                    # Place sell order at market price
                    quantity = int(self.Portfolio["SPY"].Quantity)
                    orderTicket = self.MarketOrder("SPY", -quantity)

    def OnOrderEvent(self, orderEvent):
        if orderEvent.Status == OrderStatus.Filled:
            if "TrailingStopLoss" in orderEvent.Order and orderEvent.Order["TrailingStopLoss"] == True:
                self.Debug("Trailing stop loss order filled")

