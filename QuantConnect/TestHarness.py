import datetime as dt
from typing import List
from Strategy_1 import TrendFollowingADX
from QuantConnect.Data.Market import TradeBar


class TestHarness:
    def __init__(self, start_date: dt.datetime, end_date: dt.datetime, symbols: List[str]):
        self.start_date = start_date
        self.end_date = end_date
        self.symbols = symbols

    def run(self):
        algo = TrendFollowingADX()
        algo.SetStartDate(self.start_date)
        algo.SetEndDate(self.end_date)
        algo.SetCash(100000)
        for symbol in self.symbols:
            equity = algo.AddEquity(symbol, Resolution.Daily)
        algo.Initialize()
        bar = TradeBar()
        algo.OnData(bar.Index, bar.symbol, bar.open, bar.high, bar.low, bar.close, bar.volume)
