import os
from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.models.lite_llm import LiteLlm
from ..prompts import MONGODB_CHECKER_INSTRUCTION

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is required for the MongoDB checker agent")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is required for the MongoDB checker agent")

root_agent = Agent(
    model=LiteLlm(
        model="openrouter/google/gemini-2.5-flash",
        api_key=OPENROUTER_API_KEY,
        api_base="https://openrouter.ai/api/v1"
    ),
    name="mongodb_prize_checker",
    description="Validates MongoDB prize submissions by checking for MongoDB driver usage in code.",
    instruction=MONGODB_CHECKER_INSTRUCTION,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "X-MCP-Readonly": "true",
                    "X-MCP-Toolsets": "repos,search,files"
                },
            )
        )
    ],
)
