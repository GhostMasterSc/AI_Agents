import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
import logfire

logfire.configure()
model = OpenAIModel(
    model_name="llama3.2:1b",
    base_url="http://localhost:11434/v1",
    api_key="ollama")   

class Calculation(BaseModel):
    """"Captures the result of a calculation"""
    result: int


agent = Agent(model=model,
              result_type=Calculation)

result = agent.run_sync("What is the result of 31 + 69?")

logfire.notice("Calculation result {result}", result=str(result.data))
logfire.info("Calculation result {result}", result=type(result.data))
logfire.info("Calculation result {result}", result=result.data.result)