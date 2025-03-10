from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent, RunContext
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated, List, Any
from langgraph.config import interrupt
from dotenv import load_dotenv
from openai import AsyncOpenAI
from supabase import Client
import os
import logfire

from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter
)

from pydantic_ai.models.openai import OpenAIModel