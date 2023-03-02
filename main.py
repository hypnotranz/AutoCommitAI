import openai
import os

openai.api_key = "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"
model_engine = "davinci"

prompt = "Some text to prompt the AI"

code1 = "def multiply(a, b):\n    return a * b"
code2 = "def multiply(a, b):\n    if a < 0 or b < 0:\n        raise ValueError('Inputs must be positive')\n    return a * b"

# Define the parameters for the Codex API call
parameters = {
    "model": "davinci-codex-002",
    "prompt": "Compare two code snippets:\n\nSnippet 1:\n" + code1 + "\n\nSnippet 2:\n" + code2 + "\n\nCommit details:"
}

response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
)

for choice in response.choices:
    print(choice.text)