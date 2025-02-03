from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from colorama import Fore
from dotenv import load_dotenv
import os

load_dotenv()

model_openai = OpenAIModel(model_name=os.getenv("LLM_MODEL"),
                    base_url=os.getenv("BASE_URL"),
                    api_key=os.getenv("OPENROUTER_API_KEY")
                    )   

model_ollama = OpenAIModel(
    model_name="llama3.2:1b",
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

agent_openai = Agent(model=model_openai)
agent_ollama = Agent(model=model_ollama)

response_openai = agent_openai.run_sync("What is the capital of Turkey?")


print(Fore.RED, "OpenAI Agent", response_openai.data)

message_history = response_openai.new_messages()

response_ollama = agent_ollama.run_sync("Tell me about this city", message_history = message_history)
print(Fore.GREEN, "Ollama Agent", response_ollama.data)













