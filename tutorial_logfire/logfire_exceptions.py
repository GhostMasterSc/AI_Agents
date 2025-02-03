import os
import logfire
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel


logfire.configure()

model = OpenAIModel(
    model_name="llama3.2:1b",
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

agent = Agent(model=model)

with logfire.span("Calling ollama 3.2:1b") as span:
    try:
        response = agent.run_sync("What is the capital of Turkey?")
        raise ValueError(response.data)
    except ValueError as e:
        span.record_exception(e)

       