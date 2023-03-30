from quantconnect_api import QuantConnectAPI

api = QuantConnectAPI(
    repo_url="https://github.com/my-username/my-repo.git",
    repo_dir="my-repo",
    strategy_filename="my-strategy.py"
)

api.clone_repository()
strategy_code = api.load_strategy()
api.compile_strategy(strategy_code)
api.run_backtest(start_date="2015-01-01", end_date="2021-01-01", cash=100000, symbols=[{
    "symbol": "SPY",
    "resolution": "Daily",
    "tickType": "Trade",
    "dataNormalizationMode": "SplitAdjusted"
}])
api.save_results()
api.commit_and_push()
