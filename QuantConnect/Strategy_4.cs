

# RangeTrading_BollingerBands.cs

using System;
using System.Linq;
using System.Collections.Generic;
using QuantConnect.Data.Market;
using QuantConnect.Indicators;

namespace QuantConnect.Algorithm
{
    public class RangeTradingBollingerBands : QCAlgorithm
    {
        private BollingerBands _bb;
        private decimal _upperBand;
        private decimal _lowerBand;
        private decimal _atrStop;

        public override void Initialize()
        {
            SetStartDate(2015, 1, 1);
            SetEndDate(2020, 12, 31);
            SetCash(100000);

            AddSecurity(SecurityType.Equity, "SPY", Resolution.Minute);

            int period = 20;
            decimal k = 2;

            _bb = new BollingerBands(period, k);
            RegisterIndicator("SPY", _bb, Resolution.Minute);

            _atrStop = ATR("SPY", period).Average * 0.5m; 
        }

        public void OnData(TradeBars data)
        {
            if (!_bb.IsReady) return;

            var securityHolding = Portfolio["SPY"];
            var price = data["SPY"].Close;

            if (securityHolding.Invested && (price <= _lowerBand || price >= _upperBand))
                Liquidate("SPY");

            if (!securityHolding.Invested && price > _upperBand)
                SetHoldings("SPY", 1.0m);

            if (!securityHolding.Invested && price < _lowerBand)
                SetHoldings("SPY", -1.0m);

            if (securityHolding.Invested && price >= (_upperBand - _atrStop))
                Liquidate("SPY");

            if (securityHolding.Invested && price <= (_lowerBand + _atrStop))
                Liquidate("SPY");

            
        }
    }
}