

# Momentum_Stochastic.cs

using System;
using System.Linq;
using QuantConnect.Data;
using QuantConnect.Indicators;
using QuantConnect.Orders;

namespace QuantConnect.Algorithm
{
    public class MomentumStochastic : QCAlgorithm
    {
        private Stochastic _stoch;
        private bool _inPosition;

        public override void Initialize()
        {
            SetStartDate(2010, 1, 1);
            SetEndDate(2020, 12, 31);
            SetCash(100000);

            var symbol = AddEquity("SPY", Resolution.Daily).Symbol;

            _stoch = new Stochastic("SPY", 14, 3, 3);
            RegisterIndicator(symbol, _stoch, Resolution.Daily);

            SetWarmUp(14);
        }

        public override void OnData(Slice data)
        {
            if (!_stoch.IsReady) return;

            var holdings = Portfolio[symbol].Quantity;

            if (!_inPosition)
            {
                if (_stoch.PercentK > 80 && _stoch.PercentD > 80)
                {
                    SetHoldings(symbol, -0.5);
                    _inPosition = true;
                }
                else if (_stoch.PercentK < 20 && _stoch.PercentD < 20)
                {
                    SetHoldings(symbol, 0.5);
                    _inPosition = true;
                }
            }
            else
            {
                if ((_stoch.PercentK < 50 && _stoch.PercentD < 50) || (_stoch.PercentK > 50 && _stoch.PercentD > 50))
                {
                    Liquidate(symbol);
                    _inPosition = false;
                }
                
                var stopPrice = Math.Max(_stoch.LowestLow.LastValue - ATR(symbol, 14).LastValue, symbol.Ask.Price * .95m);

                if (symbol.AskPrice <= stopPrice)
                {
                    Liquidate(symbol);
                    _inPosition = false;
                }
            }
        }
    }
}