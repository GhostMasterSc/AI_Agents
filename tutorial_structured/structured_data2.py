import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
import logfire
from dotenv import load_dotenv

load_dotenv()

logfire.configure()
model = OpenAIModel(model_name=os.getenv("LLM_MODEL_OPENAI"),
                    base_url=os.getenv("BASE_URL"),
                    api_key=os.getenv("OPENROUTER_API_KEY")
                    )    

class Capital(BaseModel):
    """Captures the capital of a country"""
    name: str
    year_founded: int
    short_history: str
    
agent = Agent(model=model,
              result_type=Capital)

result = agent.run_sync("What is the capital of Turkey?")

logfire.notice("Capital result {result}", result=str(result.data))
logfire.info("Capital result {result}", result=type(result.data))
logfire.info("Capital of Turkey {result}", result=result.data.name)
logfire.info("Capital founded {result}", result=result.data.year_founded)
logfire.info("Capital history {result}", result=result.data.short_history)