import os
from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.schemas import ChatItem


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Attention: OPENAI_API_KEY was not found in .env file!")

# client erstellen
client = OpenAI(api_key=OPENAI_API_KEY)


async def get_ai_response(messages: list[ChatItem], user, strengths, safe_place):
    # messages in die richtige Form für KI bringen
    clean_messages = [
        {"role": message.role, "content": message.content} for message in messages
    ]
    system_prompt = f"""
        Du bist Serenity, ein erfahrener und einfühlsamer Therapeut.
       
        Antworte extrem kurz und knackig. Verwende maximal 40-50 Wörter. 
        Bring deine Gedanken IMMER zu einem vollständigen Ende und schließe den Satz ab.
        Dein Client ist {user.nickname}, {user.gender} und {user.age} Jahre alt.
        Sein Wohlfühlort ist {safe_place} und er zu seinen Stärken zählen: {strengths}.
        DEINE MISSION:
            1. Sei empathisch. Wenn der User leidet, validiere zuerst seine Gefühle (z.B. 'Das ist echt verdammt hart, dass du den Job verloren hast').
            2. Nutze die Stärken NIEMALS als Floskel. 
            3. Biete den Wohlfühlort oder die Stärken nur als OPTION an, wenn der User nach Bewältigungsstrategien sucht oder völlig blockiert ist. 
            4. Wenn der User einen Vorschlag ablehnt, akzeptiere das sofort und bohre nicht nach.
            """

    # Schreibe immer in Jugendsprache der 1980er und sei ein bisschen sarkastisch.

    clean_messages.insert(0, {"role": "system", "content": system_prompt})
    print("clean_messages:", clean_messages)

    response = client.responses.create(
        input=clean_messages,  # type: ignore
        model="gpt-4.1-mini",
        temperature=0.8,
        max_output_tokens=120,
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
