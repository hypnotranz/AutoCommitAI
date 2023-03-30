

# Strategy_19.cs

using System;
using System.Linq;
using QuantConnect.Data.Market;
using QuantConnect.Indicators;

namespace QuantConnect.Algorithm
{
    public class TrendFollowingStrategy : QCAlgorithm
    {
        private MovingAverageConvergenceDivergence _macd;
        private ExponentialMovingAverage _emaFast;
        private ExponentialMovingAverage _emaSlow;
        private RollingWindow<decimal> _ribbon;

        private Symbol _symbol;

        public override void Initialize()
        {
            SetStartDate(2010, 1, 1);
            SetEndDate(DateTime.Now.Date.AddDays(-1));
            SetCash(100000);

            _symbol = AddEquity("SPY", Resolution.Daily).Symbol;

            var fastPeriod = 12;
            var slowPeriod = 26;

            _macd = MACD(_symbol, fastPeriod, slowPeriod, 9);
            _emaFast = EMA(_symbol, fastPeriod);
            _emaSlow = EMA(_symbol, slowPeriod);

            var ribbonPeriods = new[] { 10, 20, 30, 40 };
            var ribbonWindowSize = ribbonPeriods.Max();

            _ribbon = new RollingWindow<decimal>(ribbonWindowSize);

            foreach (var period in ribbonPeriods)
            {
                var ema = EMA(_symbol, period);
                ema.Updated += (sender, args) =>
                {
                    if (_ribbon.IsReady)
                    {
                        // remove the oldest value from the ribbon
                        _ribbon.Remove(_ribbon[0]);
                    }

                    // add the new value to the ribbon
                    _ribbon.Add(ema.Current.Value);

                    if (_ribbon.IsReady && IsCrossover())
                    {
                        Buy(_symbol, CalculateOrderQuantity(_symbol.Symbol));
                    }
                };
            }
        }

        public override void OnData(Slice data)
        {
            if (!_macd.IsReady || !_emaFast.IsReady || !_emaSlow.IsReady)
                return;

            // check for exit criteria
            if (IsExitSignal() || IsStopHit())
                Sell(_symbol, Portfolio[_symbol].Quantity);

            // update trailing stop order
             UpdateTrailingStopOrder();
       }

       private bool IsCrossover()
       {
           return Math.Sign(_ribbon[0] - _emaFast) != Math.Sign(_ribbon[0] - _emaSlow);
       }

       private bool IsExitSignal()
       {
           return !Portfolio.Invested ||
                  (Portfolio.Invested &&
                   Math.Sign(_macd.Signal - _macd.Current.Value) !=
                   Math.Sign(_macd.Signal - _macd.Previous.Value));
       }

       private bool IsStopHit()
       {
           return Portfolio.Invested &&
                  (Securities[_symbol].Close - Securities[_symbol].High) <= Securities[_symbol].ATR(14) * -1m;
       }

       private void UpdateTrailingStopOrder()
       {
           var openOrders = Transactions.GetOpenOrders(_symbol);
           foreach (var order in openOrders.Where(order => order.Type == OrderType.StopMarket))
           {
               CancelOrder(order.Id);
           }

           if (!Portfolio.Invested) return;

           var currentPrice = Securities[_symbol].Close;
           var atrMultiple = 1m;

           if (_macd.IsReady && Portfolio[_symbol].UnrealizedProfitPercent > atrMultiple * Securities[_symbol].ATR(14))
               atrMultiple += Portfolio[_symbol].UnrealizedProfitPercent / Securities[_symbol].ATR(14);

           atrMultiple += 0.5m; // adding cushion

           var stopPrice = currentPrice - atrMultiple * Securities[_symbol].ATR(14);

           StopMarketOrder(_symbol, CalculateOrderQuantity(_symbol.Symbol), stopPrice,
               "Trailing Stop Loss Order");
      }
   }
}