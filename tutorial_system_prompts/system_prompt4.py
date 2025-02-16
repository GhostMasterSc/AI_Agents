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

class SystemPrompt(BaseModel):
    """System prompt for the agent"""
    prompt: str
    tags: list[str]


prompt_agent = Agent(model=model, result_type=SystemPrompt, system_prompt="You an expert prompt writer. Create a system prompt to be used for an AI agent that will help a user based on the user's input. Must be very descriptive and include step by step instructions on how the agent can best answer user's question. Do not directly answer the question. Start with 'You are a helpful assistant specialized in...'. Include any relevant tags that will help the AI agent understand the context of the user's input.")

agent = Agent(model=model, system_prompt="Use the system prompt and tags provided to generate a helpful response to the user's input.")

@agent.system_prompt
def add_prompt(ctx: RunContext[SystemPrompt]) -> str:
    return ctx.deps.prompt

@agent.system_prompt
def add_tags(ctx: RunContext[SystemPrompt]) -> str:
    return f"Use the following tags: {ctx.deps.tags}"

def main_loop():
    message_history = []
    prompt_generated = False

    while True:
        user_input = input("Enter a user prompt: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        if not prompt_generated:
            result = prompt_agent.run_sync(user_prompt=user_input).data
            
            print(f"Generated prompt: {result.prompt}")
            print(f"Tags: {result.tags}")
            prompt_generated = True

        response = agent.run_sync(user_prompt=user_input, deps=result, message_history=message_history)
        print(f"Response: {response.data}")
        message_history = response.all_messages()

if __name__ == "__main__":
    main_loop()
    