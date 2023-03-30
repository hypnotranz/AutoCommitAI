

# Strategy_TrendFollowing_IchimokuClouds.cs

using System;
using System.Linq;
using QuantConnect.Algorithm.Framework;
using QuantConnect.Algorithm.Framework.Alphas;
using QuantConnect.Algorithm.Framework.Execution;
using QuantConnect.Algorithm.Framework.Portfolio;
using QuantConnect.Algorithm.Framework.Risk;
using QuantConnect.Data.Market;
using QuantConnect.Indicators;

namespace QuantConnect.Algorithm.CSharp
{
    public class TrendFollowingIchimokuClouds : QCAlgorithm
    {
        private IchimokuKinkoHyo _ichimoku;

        public override void Initialize()
        {
            SetStartDate(2010, 1, 1);
            SetEndDate(DateTime.Now.Date.AddDays(-1));
            SetCash(100000);

            AddEquity("SPY", Resolution.Daily);

            _ichimoku = new IchimokuKinkoHyo("Ichimoku");
            RegisterIndicator("SPY", _ichimoku, Resolution.Daily);
        }

        public override void OnData(Slice data)
        {
            if (!_ichimoku.IsReady) return;

            var holdings = Portfolio["SPY"].Quantity;

            if (holdings <= 0)
            {
                if (data["SPY"].Close > _ichimoku.Conversion && data["SPY"].Close > _ichimoku.Base)
                {
                    SetHoldings("SPY", 1);
                }
                else if (data["SPY"].Close > _ichimoku.Conversion && data["SPY"].Close < _ichimoku.Base)
                {
                    SetHoldings("SPY", 0.5);
                }
                else if (data["SPY"].Close < _ichimoku.Conversion && data["SPY"].Close < _ichimoku.Base)
                {
                    SetHoldings("SPY", -1);
                }
                else if (data["SPY"].Close < _ichimoku.Conversion && data["SPY"].Close > _ichimoku.Base)
                {
                    SetHoldings("SPY", -0.5);
                }
            }
            else
            {
                if ((holdings > 0 && (data["SPY"].Close < Math.Min(_ichimoku.Conversion, _ichimoku.Base) || 
                    data["SPY"].Close < _ichimoku.SpanA || data["SPY"].Close < _ichimoku.SpanB)) ||
                    (holdings < 0 && (data["SPY"].Close > Math.Max(_ichimoku.Conversion, _ichimoku.Base) || 
                    data["SPY"].Close >_ ichimoku.SpanA || data["SPY"].Close >_ ichimoku.SpanB)))
                {
                    Liquidate("SPY");
                }
                
                 var atr = ATR("SPY", 14).Current.Value;
                 var stopPrice = holdings > 0 ? Math.Max(data["SPY"].Low, Portfolio.TotalUnrealizedProfit / atr + data["Spy"].Low) :
                     Math.Min(data ["Spy"] .High, Portfolio.TotalUnrealizedProfit / atr + data ["Spy"] .High);

                 SetStopMarketOrder ("Spy" , holdings , stopPrice );
             }

             PlotIndicator(_ichmouk , " Ichmouk " );
         }
     }
 }