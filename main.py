from codex_api import CodexAPI
import os


api = CodexAPI("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", "code-davinci-002")

code1 = "def multiply(a, b):\n    return a * b"
code2 = "def multiply(a, b):\n    if a < 0 or b < 0:\n        raise ValueError('Inputs must be positive')\n    return a * b"
description = "Description of changes"

generated_code = api.generate_diff_description(code1, code2, description)
print(generated_code)