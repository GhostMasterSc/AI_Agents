from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from colorama import Fore

model = OpenAIModel(
    model_name="llama3.2:1b",
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

agent = Agent(model=model)

response = agent.run_sync("What is the capital of Turkey?")
print(Fore.RED, response.data)













