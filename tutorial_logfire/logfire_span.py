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

with logfire.span("Calling ollama 3.2:1b") as span:    
    agent = Agent(model=model)
    result = agent.run_sync("What is the capital of Turkey?")
    span.set_attribute("result", result.data)
    logfire.notice("Ollama 3.2:1b response", result=result.data)
    logfire.info("Ollama 3.2:1b response", result=result.data)
    logfire.debug("Ollama 3.2:1b response", result=result.data)
    logfire.warn("Ollama 3.2:1b response", result=result.data)
    logfire.error("Ollama 3.2:1b response", result=result.data)
    logfire.fatal("Ollama 3.2:1b response", result=result.data)


