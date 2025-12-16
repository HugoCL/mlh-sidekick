from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.models.lite_llm import LiteLlm
from ..prompts import GEMINI_CHECKER_INSTRUCTION

GITHUB_TOKEN = ""
OPENROUTER_API_KEY = "sk-or-v1-"

root_agent = Agent(
     model=LiteLlm(
        model="openrouter/google/gemini-2.5-flash",
        api_key=OPENROUTER_API_KEY,
        api_base="https://openrouter.ai/api/v1"
    ),
    name="gemini_prize_checker",
    description="Validates Gemini prize submissions by checking Project Numbers and API usage in code.",
    instruction=GEMINI_CHECKER_INSTRUCTION,
    tools=[
        McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url= "https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-MCP-Readonly": "true",
            "X-MCP-Toolsets": "repos,search,files"
        },
    )
)

    ],
)