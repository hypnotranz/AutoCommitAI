

# Strategy_TrendFollowing.cs

using System;
using System.Collections.Generic;
using System.Linq;
using QuantConnect.Algorithm.Framework;
using QuantConnect.Algorithm.Framework.Alphas;
using QuantConnect.Algorithm.Framework.Execution;
using QuantConnect.Algorithm.Framework.Portfolio;
using QuantConnect.Algorithm.Framework.Selection;
using QuantConnect.Data.Market;
using QuantConnect.Indicators;

namespace QuantConnect.Algorithm.CSharp
{
    public class TrendFollowingStrategy : QCAlgorithm
    {
        private ParabolicStopAndReverse _parabolicSAR;

        public override void Initialize()
        {
            SetStartDate(2010, 1, 1);
            SetEndDate(2020, 12, 31);
            SetCash(100000);

            AddEquity("SPY", Resolution.Daily);

            _parabolicSAR = new ParabolicStopAndReverse("SAR", 0.02m, 0.2m);
        }

        public override void OnData(Slice data)
        {
            if (!Portfolio.Invested)
            {
                if (data["SPY"].Close > _parabolicSAR.Current.Value)
                {
                    SetHoldings("SPY", 1);
                }
            }
            else
            {
                if (data["SPY"].Close < _parabolicSAR.Current.Value)
                {
                    Liquidate("SPY");
                }
            }
        }

        public override void OnEndOfDay()
        {
            Plot("Indicator", "Parabolic SAR", _parabolicSAR.Current.Value);
        }
    }
}