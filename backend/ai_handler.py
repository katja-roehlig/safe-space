import os
from dotenv import load_dotenv
from openai import OpenAI

from schemas import ChatItem


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Attention: OPENAI_API_KEY was not found in .env file!")

# client erstellen
client = OpenAI(api_key=OPENAI_API_KEY)


async def get_ai_response(messages: list[ChatItem]):
    # messages in die richtige Form für KI bringen
    clean_messages = [
        {"role": message.role, "content": message.content} for message in messages
    ]
    system_prompt = "Du bist ein erfahrener und einfühlsamer Therapeut. Schreibe immer in Jugendsprache der 1980er und sei ein bisschen sarkastisch."
    clean_messages.insert(0, {"role": "system", "content": system_prompt})
    print("clean_messages:", clean_messages)

    response = client.responses.create(
        input=clean_messages,  # type: ignore
        model="gpt-4.1-mini",
        temperature=0.8,
        max_output_tokens=80,
    )
    tokens = response.usage

    input_tokens = tokens.input_tokens if tokens else 0
    cached_tokens = tokens.input_tokens_details.cached_tokens if tokens else 0
    output_tokens = tokens.output_tokens if tokens else 0

    return (
        response.output_text,
        input_tokens,
        cached_tokens,
        output_tokens,
    )

    # print("Output-Tokens: ", response.usage.output_tokens)  # type: ignore


# print("Input", response.usage.input_tokens)  # type: ignore
# print("Input", response.usage.input_tokens_details.cached_tokens)  # type: ignore
# print("Input", response.usage.output_tokens)  # type: ignore
