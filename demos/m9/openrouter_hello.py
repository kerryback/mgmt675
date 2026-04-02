"""
Step 3 Demo: Send a single message to a model via OpenRouter.

Usage:
    Set your OpenRouter API key as an environment variable:
        export OPENROUTER_API_KEY=sk-or-...

    Then run:
        python openrouter_hello.py
"""

import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

response = client.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    messages=[
        {"role": "user", "content": "Explain a P/E ratio in two sentences."}
    ],
)

print(response.choices[0].message.content)
