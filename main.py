from codex_api import CodexAPI
import os
import csv

api = CodexAPI("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", "code-davinci-002")

indicator_strategy_tuples = []

with open('indicator_strategy_list.csv', newline='') as f:
    reader = csv.reader(f)
    # Iterate over each row in the CSV file
    for row in reader:
        # Extract the indicator, strategy, entry signal, stop signal, and exit signal from the row
        indicator, strategy, entry_signal, stop_signal, exit_signal = row
        # Add the indicator, strategy, entry signal, stop signal, and exit signal to the tuple list
        indicator_strategy_tuples.append((indicator, strategy, entry_signal, stop_signal, exit_signal))
        # Print the row that was just added to the list
        print(
            f"Indicator: {indicator}, Strategy: {strategy}, Entry Signal: {entry_signal}, Stop Signal: {stop_signal}, Exit Signal: {exit_signal}")

indicator_strategy_tuples = [("SMA", "mean reversion"), ("RSI", "momentum")]

for indicator, strategy in indicator_strategy_tuples:
    prompt = f"Create a QuantConnect strategy that implements Strategy: {strategy} using Indicator {indicator}., "

    generated_code = api.generate_response(prompt)
    print(generated_code)

code1 = "def multiply(a, b):\n    return a * b"
code2 = "def multiply(a, b):\n    if a < 0 or b < 0:\n        raise ValueError('Inputs must be positive')\n    return a * b"
description = "Description of changes"

generated_code = api.generate_diff_description(code1, code2, description)
print(generated_code)
