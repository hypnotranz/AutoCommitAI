

# TrendFollowingADX.cs

using System;
using System.Linq;
using QuantConnect.Data;
using QuantConnect.Indicators;

namespace QuantConnect.Algorithm.CSharp
{
    public class TrendFollowingADX : QCAlgorithm
    {
        private AverageDirectionalIndex _adx;
        private RollingWindow<IndicatorDataPoint> _adxWindow;

        private Security _security;

        public override void Initialize()
        {
            SetStartDate(2015, 1, 1);
            SetEndDate(DateTime.Now.Date.AddDays(-1));
            SetCash(100000);

            _security = AddEquity("SPY", Resolution.Daily).Symbol;

            _adx = ADX(_security, 14);

            _adxWindow = new RollingWindow<IndicatorDataPoint>(2);
        }

        public override void OnData(Slice data)
        {
            if (!data.ContainsKey(_security))
                return;

            var price = data[_security].Close;

            if (!_adx.IsReady)
                return;

            _adxWindow.Add(_adx.Current);

            if (_adxWindow.Count < 2)
                return;

            var previousAdx = _adxWindow[0];
            var currentAdx = _adxWindow[1];

            var above20 = currentAdx.Value > 20;
            var below20 = currentAdx.Value < 20;
            
			var isLongPosition = Portfolio[_security].IsLong;
			var isShortPosition = Portfolio[_security].IsShort;
			var isFlatPosition = !isLongPosition && !isShortPosition;

			if (above20 && isFlatPosition)
			{
				SetHoldings(_security, 1.0);
				Debug($"BUY {_security} at {price}");
			}
			else if (below20 && isFlatPosition)
			{
				SetHoldings(_security, -1.0);
				Debug($"SHORT {_security} at {price}");
			}
			else if ((below20 && isLongPosition) || (above20 && isShortPosition))
			{
				Liquidate(_security);
				Debug($"EXIT {_security} at {price}");
			}

        	if (isLongPosition || isShortPosition)
        	{
            	var highPrice = data[_security].High;
            	var lowPrice = data[_security].Low;

            	if (isLongPosition && currentAdx.Value < previousAdx.Value && highPrice < price - ATR(_security, 14).Current * 2)
            	{
                	Liquidate(_security);
                	Debug($"STOP LOSS LONG {_security} at {price}");
            	}
            	else if (isShortPosition && currentAdx.Value < previousAdx.Value && lowPrice > price + ATR(_security, 14).Current * 2)
            	{
                	Liquidate(_security);
                	Debug($"STOP LOSS SHORT {_security} at {price}");
            	}
        	}
    	}
    }
}