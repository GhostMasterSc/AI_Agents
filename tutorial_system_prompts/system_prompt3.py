import os
from datetime import date
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel

load_dotenv()

model = OpenAIModel(model_name=os.getenv("LLM_MODEL_OPENAI"),
                    base_url=os.getenv("BASE_URL"),
                    api_key=os.getenv("OPENROUTER_API_KEY")
                    )

class Capital(BaseModel):
    """"Capital city model - incldues name, year founded, short history of the city and comparison to another city"""
    
    name: str
    year_founded: int
    short_history: str
    comparison: str


agent = Agent(model=model, result_type=Capital, system_prompt="You are an experienced historian and you are asked a question about the capital of a country. You are expected to provide the name of the capital city, the year it was founded, and a short history of the city. Provide an age and historical significance comparison of the cities.")

@agent.system_prompt
def add_comparison(ctx: RunContext[str]) -> str:
    return f"The city to compare to is{ctx.deps}"


result = agent.run_sync(user_prompt="What is the capital of Turkey?", deps="Paris")

print(result.data)