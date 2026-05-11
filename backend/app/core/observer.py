import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

load_dotenv()


def simple_mask(data, **kwargs):  # Das **kwargs ist das, was Pylance gefehlt hat
    return "<masked>"


langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL"),
    mask=simple_mask,
)

langfuse_handler = CallbackHandler()
