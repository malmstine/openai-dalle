import os

import openai

token = os.environ.get("OPENAI_KEY")
openai.api_key = token


def generate_images(prompt) -> str:
    res = openai.images.generate(
        model="dall-e-3",
        size="1024x1024",
        n=1,
        prompt=prompt
    )
    return res.data[0].url

