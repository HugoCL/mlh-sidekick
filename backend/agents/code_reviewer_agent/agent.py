import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.models.lite_llm import LiteLlm
from ..prompts import CODE_REVIEWER_INSTRUCTION

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is required for the code reviewer agent")

root_agent = Agent(
     model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="openrouter/google/gemini-2.5-flash",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    name="root_agent",
    description="Evaluates GitHub code samples against rubric and produces structured JSON",
    instruction=CODE_REVIEWER_INSTRUCTION,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "X-MCP-Readonly": "true",
                    "X-MCP-Toolsets": "repos,issues,pull_requests,users,code_security,dependabot",
                },
            )
        )
    ],
)