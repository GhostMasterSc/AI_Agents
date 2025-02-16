import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()


model = OpenAIModel(model_name=os.getenv("LLM_MODEL_OPENAI"),
                    base_url=os.getenv("BASE_URL"),
                    api_key=os.getenv("OPENROUTER_API_KEY")
                    )

system_prompt = """
You are an experienced React developer. Create code that meets user's requirements.
"""

agent = Agent(
    model=model,
    system_prompt=system_prompt,
)

result = agent.run_sync(user_prompt="Create a functional React component that displays a user progile with the following details: name, email, and profile picture. Must use Zustand for state management and Tailwind CSS for styling.")

print(result.data)