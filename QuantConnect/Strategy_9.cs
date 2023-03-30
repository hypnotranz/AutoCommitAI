

# TrendFollowing_AroonIndicator.cs

using System;
using System.Linq;
using System.Collections.Generic;
using QuantConnect.Data;
using QuantConnect.Indicators;

namespace QuantConnect.Algorithm
{
    public class TrendFollowing_AroonIndicator : QCAlgorithm
    {
        private Aroon _aroon;

        public override void Initialize()
        {
            SetStartDate(2010, 1, 1);
            SetEndDate(DateTime.Now.Date.AddDays(-1));
            SetCash(100000);

            AddEquity("SPY", Resolution.Daily);

            _aroon = new Aroon("SPY", 25);
        }

        public override void OnData(Slice data)
        {
            if (!_aroon.IsReady) return;

            var holdings = Portfolio["SPY"].Quantity;
            var price = data["SPY"].Close;

            if (holdings <= 0 && _aroon.AroonUp > _aroon.AroonDown)
            {
                SetHoldings("SPY", 1);
                Debug("Buy >> " + price);
                return;
            }

            if (holdings >= 0 && _aroon.AroonUp < _aroon.AroonDown)
            {
                Liquidate("SPY");
                Debug("Sell >> " + price);
                return;
            }
        }
    }
}