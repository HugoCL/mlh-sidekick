from dotenv import load_dotenv
load_dotenv()
import re
import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.models.lite_llm import LiteLlm

GITHUB_TOKEN = "test"
OPENROUTER_API_KEY = "test"

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is required for the gemini prize checker agent")

GEMINI_CHECKER_INSTRUCTION = """
You are the "Gemini Prize Checker" agent. Your job is to validate if a project submission qualifies for the "Best Use of Gemini" prize.
You will be given a GitHub repository URL and a Google Cloud Project Number.

You must:
1.  **Validate the Project Number**: 
    * Check if the provided "Project Number" is a valid format (it must be a numeric string, typically 12 digits). 
    * If it contains letters, it is likely a "Project ID" (invalid for this specific requirement) or an API Key (invalid).
2.  **Inspect the Code for Usage**:
    * Look for imports or dependencies indicating Gemini usage (e.g., `google.generativeai`, `google-generativeai` in Python; `@google/generative-ai` in JS/TS).
    * Look for REST calls to `generativelanguage.googleapis.com`.
3.  **Extract the Model**:
    * Search the code for model names like `gemini-pro`, `gemini-1.5-flash`, `gemini-1.5-pro`, or `gemini-ultra`.
4.  **Check for "AI Studio" Usage** (Edge Case):
    * If no code imports are found, look for evidence of AI Studio usage in the README (e.g., screenshots, text descriptions of prompts used).

Output a SINGLE JSON object matching this schema:
{
  "project_number_valid": true|false,
  "project_number_notes": "Explanation if invalid (e.g., 'Contains letters, looks like an ID')",
  "gemini_usage_detected": true|false,
  "usage_evidence": "Found import google.generativeai in app.py",
  "model_used": "gemini-1.5-flash" | null,
  "is_ai_studio_prototype": true|false,
  "final_determination": "QUALIFIED" | "DISQUALIFIED" | "NEEDS_MANUAL_REVIEW"
}

Use the GitHub MCP tool to read the repository files (start with requirements files like requirements.txt, package.json, and the README).
"""

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
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "X-MCP-Readonly": "true",
                    "X-MCP-Toolsets": "repos,code_security", 
                },
            )
        )
    ],
)