import os
from typing import List, Dict
import git
import requests
import json
import time

class QuantConnectAPI:
    def __init__(self, repo_url: str, repo_dir: str, strategy_filename: str):
        self.repo_url = repo_url
        self.repo_dir = repo_dir
        self.strategy_filename = strategy_filename
        self.strategy_code = ""
        self.project_id = ""
        self.backtest_id = ""
        self.results = {}

    def clone_repository(self):
        # Clone the GitHub repository
        git.Repo.clone_from(self.repo_url, self.repo_dir)

    def load_strategy(self):
        # Load the strategy code from the file system
        with open(os.path.join(self.repo_dir, self.strategy_filename), "r") as f:
            self.strategy_code = f.read()

    def compile_strategy(self):
        # Compile the strategy code on QuantConnect
        r = requests.post("https://www.quantconnect.com/api/v2/projects/create", json={
            "projectId": "my-project",
            "files": [{
                "name": self.strategy_filename,
                "content": self.strategy_code
            }]
        })
        self.project_id = r.json()["projectId"]

        # Wait for the project to compile
        while True:
            r = requests.get(f"https://www.quantconnect.com/api/v2/projects/{self.project_id}")
            status = r.json()["status"]
            if status == "CompileSuccess":
                break
            elif status == "CompileError":
                print("Compilation failed.")
                exit(1)
            time.sleep(1)

    def run_backtest(self, start_date: str, end_date: str, cash: float, symbols: List[Dict[str, str]]):
        # Run a backtest on QuantConnect
        r = requests.post(f"https://www.quantconnect.com/api/v2/projects/{self.project_id}/backtests/create", json={
            "backtestName": "My Backtest",
            "settings": {
                "startDate": start_date,
                "endDate": end_date,
                "cash": cash,
                "symbols": symbols
            },
            "parameters": {},
            "notebook": {
                "language": "python"
            }
        })
        self.backtest_id = r.json()["backtestId"]

        # Wait for the backtest to complete
        while True:
            r = requests.get(f"https://www.quantconnect.com/api/v2/backtests/{self.backtest_id}/status")
            status = r.json()["status"]
            if status == "Completed":
                break
            elif status == "Failed":
                print("Backtest failed.")
                exit(1)
            time.sleep(1)

    def save_results(self):
        # Get the backtest results from QuantConnect
        r = requests.get(f"https://www.quantconnect.com/api/v2/backtests/{self.backtest_id}/results")
        self.results = r.json()

        # Save the backtest results to a file
        with open(os.path.join(self.repo_dir, "backtest-results.json"), "w") as f:
            json.dump(self.results, f)

    def commit_and_push(self):
        # Commit and push the changes to the GitHub repository
        repo = git.Repo(self.repo_dir)
        repo.git.add("--all")
        repo.index.commit("Update backtest results")
        repo.remotes.origin.push()

# Instantiate the API object
api = QuantConnectAPI(
    repo_url="https://github.com/my-username/my-repo.git",
    repo_dir="my-repo",
    strategy_filename="my-strategy.py"
)