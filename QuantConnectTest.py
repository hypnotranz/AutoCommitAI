from typing import Type
import os
from importlib import import_module
from unittest import TestCase
import logging

# Define the path to the folder containing the QuantConnect strategies
QUANTCONNECT_PATH = "./QuantConnect"

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class StrategyTestCase(TestCase):
    def __init__(self, strategy):
        super().__init__()
        self.strategy = strategy

    def runTest(self):
        # Initialize the strategy with a backtest
        self.strategy.Initialize()
        # Assert that the strategy's name matches the expected format
        self.assertRegex(self.strategy.Name, r"^Strategy_\d+$")


if __name__ == '__main__':
    # Iterate over each file in the QuantConnect folder
    for file_name in os.listdir(QUANTCONNECT_PATH):

        logging.debug(f"Filename: {file_name}")
        if file_name.endswith(".py"):
            # Get the name of the strategy from the file name
            strategy_name = os.path.splitext(file_name)[0]
            # Import the module containing the strategy
            module = import_module(f"{QUANTCONNECT_PATH}.{strategy_name}")
            # Get the strategy class from the module
            strategy_class: Type[QCAlgorithm] = getattr(module, strategy_name.capitalize())
            logging.debug(f"Strategy class type: {type(strategy_class)}")
            # Create an instance of the strategy
            strategy: QCAlgorithm = strategy_class()
            logging.debug(f"Strategy instance type: {type(strategy)}")
            # Check the types of the strategy class and instance
            assert isinstance(strategy_class, type)
            assert isinstance(strategy, QCAlgorithm)
            # Run a unit test on the strategy
            test = StrategyTestCase(strategy)
            test.run()
            print(f"Unit test passed for {strategy_name}")
