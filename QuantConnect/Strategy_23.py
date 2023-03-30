

# Strategy_TrendFollowing.py

from SuperTrend import SuperTrend
from System import *
from QuantConnect import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Orders import OrderStatus
from QuantConnect.Orders.Fees import ConstantFeeModel
from QuantConnect.Orders.Fills import ImmediateFillModel
from QuantConnect.Algorithm.Framework.Alphas.Trend import *
from QuantConnect.Algorithm.Framework.Execution.ImmediateExecutionModel import ImmediateExecutionModel
from QuantConnect.Algorithm.Framework.Portfolio.EqualWeightingPortfolioConstructionModel import EqualWeightingPortfolioConstructionModel


class TrendFollowing(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage,
                               AccountType.Margin)

        # Define the securities to be traded
        self.tickers = ['SPY']
        for ticker in self.tickers:
            equity = self.AddEquity(ticker, Resolution.Daily)
            equity.SetDataNormalizationMode(DataNormalizationMode.Raw)

        # Add the SuperTrend indicator to the chart
        indicatorPeriod = 10
        atrPeriod = 14
        multiplier = 2.0
        superTrendIndicator = SuperTrend(indicatorPeriod, atrPeriod, multiplier)
        self.PlotIndicator("SuperTrend", superTrendIndicator)

        # Use the SuperTrend as the primary indicator for trend following strategy
        superTrendCrossAboveThreshold = IndicatorCrossAbove(superTrendIndicator.SuperTrendUpperBand,
                                                            equity.Price,
                                                            timedelta(days=1))
        superTrendCrossBelowThreshold = IndicatorCrossBelow(superTrendIndicator.SuperTrendLowerBand,
                                                             equity.Price,
                                                             timedelta(days=1))
        
         # Define Alpha Model to generate buy signals when price crosses above upper band and sell signals when price crosses below lower band.
         alpha_model = InsightManager(CompositeAlphaModel(
                TrendFollowingAlphaModel(
                    resolution=Resolution.Daily,
                    super_trend_cross_above_threshold=super_trend_cross_above_threshold,
                    super_trend_cross_below_threshold=super_trend_cross_below_threshold),
                NullAlphaModel()))

         # Define Portfolio Construction Model as Equal Weighting Portfolio Construction Model.
         portfolio_construction_model = EqualWeightingPortfolioConstructionModel()

         # Define Execution Model as Immediate Execution Model.
         execution_model = ImmediateExecutionModel()

         # Set up fee and fill models.
         fee_model = ConstantFeeModel(0)
         fill_model = ImmediateFillModel()

         # Set up algorithm with defined models.
         self.SetUniverseSelection(self.UniverseSelection.None)
         self.SetAlpha(alpha_model)
         self.SetPortfolioConstruction(portfolio_construction_model)
         self.SetExecution(execution_model)
         self.SetRiskManagement(TrailingStopRiskManagementModel(1.0))  # Set stop criteria as 1 x ATR.

    def OnData(self, data):
            pass