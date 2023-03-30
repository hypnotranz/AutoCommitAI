

# TrendFollowing_MACD.cs

using System;
using System.Linq;
using QuantConnect.Data.Market;
using QuantConnect.Indicators;

namespace QuantConnect.Algorithm
{
    public class TrendFollowing_MACD : QCAlgorithm
    {
        private MovingAverageConvergenceDivergence _macd;
        private ExponentialMovingAverage _signal;
        private RelativeStrengthIndex _rsi;

        private string _symbol = "SPY";
        private decimal _atrStop = 1m;

        public override void Initialize()
        {
            SetStartDate(2010, 1, 1);
            SetEndDate(DateTime.Now.Date.AddDays(-1));
            SetCash(100000);
            AddEquity(_symbol, Resolution.Daily);

            _macd = MACD(_symbol, 12, 26, 9, MovingAverageType.Exponential);
            _signal = EMA(_macd.Signal, 9);
            _rsi = RSI(_symbol, 14);

            // set warmup period to ensure indicators are ready
            int warmupPeriod = Math.Max(_macd.Signal.WarmUpPeriod + _signal.WarmUpPeriod, _rsi.WarmUpPeriod);
            SetWarmUp(TimeSpan.FromDays(warmupPeriod));
        }

        public override void OnData(Slice data)
        {
            if (!Portfolio.Invested)
            {
                // enter long position on signal line cross above MACD line
                if (_macd.Current.Value > _signal.Current.Value && 
                    _macd.Current.Value < _macd.Previous.Value &&
                    !_rsi.IsOverbought())
                {
                    decimal stopPrice = data[_symbol].High * (1m - (_atrStop / 100m));
                    SetHoldings(_symbol, 1m);
                    SetStopLoss(_symbol, stopPrice);
                }
            }
            else
            {
                // exit long position on signal line cross below MACD line or trailing stop hit
                if (_macd.Current.Value < _signal.Current.Value ||
                    Portfolio[_symbol].UnrealizedProfitPercent < -_atrStop)
                {
                    Liquidate();
                }
                else
                {
                    // update stop loss based on current ATR value
                    decimal atrValue = ATR(_symbol, 14).Current.Value;
                    decimal newStopPrice = data[_symbol].High * (1m - ((atrValue * _atrStop) / 100m));
                    UpdateStopLoss(_symbol, newStopPrice);
                }
            }
        }
    }

    public static class Extensions
    {
        public static bool IsOverbought(this RelativeStrengthIndex rsi)
        {
            return rsi > 70m;
        }
    }
}