import os
import openai

api_key = "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"

openai.api_key = api_key

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)