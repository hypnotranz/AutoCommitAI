from codex_api import CodexAPI
from chat_gpt_api import ChatGptAPI
import os
import csv
import re

api_key = "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"
api = ChatGptAPI(api_key)

indicator_strategy_tuples = []

# Create QuantConnect folder if it doesn't exist
if not os.path.exists('QuantConnect'):
    os.makedirs('QuantConnect')

with open('indicator_strategy_list.csv', newline='') as f:
    reader = csv.reader(f)
    # Iterate over each row in the CSV file
    for row in reader:
        # Extract the indicator, strategy, entry signal, stop signal, and exit signal from the row
        indicator, strategy, entry_signal, stop_signal, exit_signal = row
        # Add the indicator, strategy, entry signal, stop signal, and exit signal to the tuple list
        indicator_strategy_tuples.append((indicator, strategy, entry_signal, stop_signal, exit_signal))
        # Print the row that was just added to the list
        print(f"Indicator: {indicator}, Strategy: {strategy}, Entry Signal: {entry_signal}, Stop Signal: {stop_signal}, Exit Signal: {exit_signal}")

# Initialize sequence number to 1
sequence_number = 1

for indicator, strategy, entry_signal, stop_signal, exit_signal in indicator_strategy_tuples:
    # Create file name using sequence number and strategy name
    file_name = f"Strategy_{sequence_number}.cs"
    sequence_number += 1

    prompt = f"Create a QuantConnect strategy that implements Strategy. " \
             f"Include a single comment at the top with the name of the file, like this:" \
             f"\"# {file_name}\". " \
             f"Followed by the required imports.  Do not include ANY OTHER comments or instructions." \
             f"The name of the class implementing QCAlgorithm and its implementation should reflect the following:\n\n" \
             f"Strategy: {strategy}\n" \
             f"Primary Indicator: {indicator}\n" \
             f"Entry Criteria: {entry_signal}\n" \
             f"Exit Criteria: {exit_signal}\n" \
             f"Stop Criteria: {stop_signal}\n"

    messages = [
        {"role": "user", "content": prompt}
    ]

    if os.path.exists(os.path.join('QuantConnect', file_name)):
        print(f"File for strategy {strategy} already exists. Skipping...")
        continue

    print(prompt, end='')

    response = api.generate_response(messages)

    if not response:
        print("No code generated. Skipping...")
        continue

    # Write the generated code to a file in the QuantConnect folder
    file_path = os.path.join('QuantConnect', file_name)
    with open(file_path, 'w') as f:
        f.write(response.content)

    print(response.content, end='')
    print(f"Successfully created file {file_name}.")
