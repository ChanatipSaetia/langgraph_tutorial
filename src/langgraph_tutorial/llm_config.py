# llm_config.py
# Place your LLM/model configuration here
# Example: from langchain.llms import OpenAI
# model = OpenAI(api_key="YOUR_KEY")

# Replace with your own model config
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google_vertexai",
    thinking_budget=256,
)
