import openai
import os

openai.api_key = "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"
model_engine = "code-davinci-002"

code1 = "def multiply(a, b):\n    return a * b"
code2 = "def multiply(a, b):\n    if a < 0 or b < 0:\n        raise ValueError('Inputs must be positive')\n    return a * b"

# Define the prompt for the Codex API call
prompt = f"Diff and describe changes:\n\nSnippet 1:\n{code1}\n\nSnippet 2:\n{code2}\n\nDescription:"

# Define the parameters for the Codex API call
parameters = {
    "engine": model_engine,
    "prompt": prompt,
    "max_tokens": 1000,
    "temperature": 0.5,
    "stop": None,
}

try:
    # Make the Codex API call
    response = openai.Completion.create(**parameters)

    # Print the generated code snippet
    for choice in response.choices:
        print(choice.text)

except openai.error.InvalidRequestError as e:
    print(f"Invalid Request Error: {e}")
except openai.error.AuthenticationError as e:
    print(f"Authentication Error: {e}")
except openai.error.APIConnectionError as e:
    print(f"API Connection Error: {e}")
except openai.error.OpenAIError as e:
    print(f"OpenAI Error: {e}")