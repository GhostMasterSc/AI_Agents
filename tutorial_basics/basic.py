import asyncio
import os 
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

model = OpenAIModel(model_name=os.getenv("LLM_MODEL"),
                    base_url=os.getenv("BASE_URL"),
                    api_key=os.getenv("OPENROUTER_API_KEY")
                    )   

agent = Agent(model=model,
              system_prompt="You are a helpful assistant that can answer questions and help with tasks.")


response = agent.run_sync("What is the capital of the moon?")
print(response)