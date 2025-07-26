import os
import json
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled,Runner

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, and MODEL_NAME."
    )








# --- Main Function ---

async def main():
    # Example queries to test different aspects of the system
    queries = [
        "I want to become a data scientist",
        # "Can you help me find jobs?"
        # "How do I learn SQL and Pandas?"
    ]
    
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        
        

if __name__ == "__main__":
    asyncio.run(main())
