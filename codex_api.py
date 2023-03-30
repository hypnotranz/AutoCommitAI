import openai


class CodexAPI:
    def __init__(self, api_key, model_engine):
        self.api_key = api_key
        self.model_engine = model_engine
        openai.api_key = self.api_key

    def generate_response(self, prompt: str):

        parameters = {
            "engine": "davinci-codex",
            "prompt": prompt,
            "max_tokens": 3900,
            "temperature": 0.5,
            "stop": None,
        }

        try:
            response = openai.Completion.create(**parameters)
            generated_code = response.choices[0].text
            if response.choices:
                generated_code = response.choices[0].text
                print(generated_code)
            else:
                print("No code generated")

            return generated_code

        except openai.error.InvalidRequestError as e:
            print(f"Invalid Request Error: {e}")
        except openai.error.AuthenticationError as e:
            print(f"Authentication Error: {e}")
        except openai.error.APIConnectionError as e:
            print(f"API Connection Error: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI Error: {e}")

    def generate_diff_description(self, code1, code2, description):
        prompt = f"Diff and describe changes:\n\nSnippet 1:\n{code1}\n\nSnippet 2:\n{code2}\n\nDescription:"

        parameters = {
            "engine": self.model_engine,
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.5,
            "stop": None,
        }

        try:
            response = openai.Completion.create(**parameters)
            generated_code = ''
            for choice in response.choices:
                generated_code = choice.text
            return generated_code
        except openai.error.InvalidRequestError as e:
            print(f"Invalid Request Error: {e}")
        except openai.error.AuthenticationError as e:
            print(f"Authentication Error: {e}")
        except openai.error.APIConnectionError as e:
            print(f"API Connection Error: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI Error: {e}")