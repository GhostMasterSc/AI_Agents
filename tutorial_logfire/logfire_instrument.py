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

@logfire.instrument("Applying multiply to {x=} and {y=}")
def multiply(x: int, y: int) -> int:
    return x * y

with logfire.span("Calling ollama 3.2:1b") as span:
    try:
        result = agent.run_sync(f"Can you confirm that {multiply(10, 20)} is the product of 10 and 20? Also, include answer?")
        span.set_attribute("result", result.data)
    except ValueError as e:
        span.record_exception(e)
        






