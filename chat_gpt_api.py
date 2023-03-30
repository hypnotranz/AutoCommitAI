import openai

class ChatGptAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_response(self, messages):
        parameters = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.8,
            "top_p": 0.9,
            "n": 3,
         #   "stream": false,
            "stop": "Thank you.",
            "max_tokens": 1000,
            "presence_penalty": -0.5,
            "frequency_penalty": 0.5,
           # "logit_bias": {"Paris": 100},
            "user": "1234abcd"
        }

        try:
            response = openai.ChatCompletion.create(**parameters)
            if response.choices:
                generated_text = response.choices[0].message
                print(generated_text)
            else:
                print("No text generated")
                generated_text = ""
            return generated_text

        except openai.error.InvalidRequestError as e:
            print(f"Invalid Request Error: {e}")
        except openai.error.AuthenticationError as e:
            print(f"Authentication Error: {e}")
        except openai.error.APIConnectionError as e:
            print(f"API Connection Error: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI Error: {e}")

if __name__ == '__main__':
    api_key = "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"

    chat_api = ChatGptAPI(api_key)

    prompt = "implement a function that takes a graph and returns a list of nodes in the order they should be " \
             "visited. Do this in python.  Return ONLY CODE.  do not return comments or descriptions! Do not return anything telling me that the code is about to come.  imports and Code only! There should be a single comment at the first line in the file # filename='graph.py'"

    messages = [
        {"role": "user", "content": prompt},
    #     {"role": "system", "content": prompt},
    #    {"role": "assistant", "content": prompt},
    ]

    generate_response = chat_api.generate_response(messages)