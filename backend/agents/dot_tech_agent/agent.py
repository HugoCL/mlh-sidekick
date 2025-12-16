import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from ..prompts import DOT_TECH_INSTRUCTION

load_dotenv()

OPENROUTER_API_KEY = "sk-or-v1-"

def check_website_status(url: str) -> str:
    url = url.strip()   
    if not url.startswith("http"):
        url = "https://" + url     
    try:
        response = requests.get(url, timeout=10)
        return f'{{"status_code": {response.status_code}, "reachable": true}}'
    except Exception as e:
        return f'{{"reachable": false, "error": "{str(e)}"}}'

tech_agent = Agent(
    model=LiteLlm(
        # Using 1.5 Pro to ensure stable tool execution
        model="openrouter/google/gemini-2.5-flash",
        api_key=OPENROUTER_API_KEY,
        api_base="https://openrouter.ai/api/v1"
    ),
    name="dot_tech_prize_checker",
    description="Validates .Tech prize submissions by checking TLD and website uptime.",
    instruction=DOT_TECH_INSTRUCTION,
    tools=[check_website_status] 
)