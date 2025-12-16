import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

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

DOT_TECH_INSTRUCTION = """
You are the ".Tech Prize Checker" agent. Your goal is to validate if a project submission qualifies for the "Best .Tech Domain" prize.
You will be given a domain URL (string).

**Context on TLDs:**
There are dozens of available Top-Level Domains (TLDs) including: .us, .biz, .tv, .courses, .study, .club, .design, .compare, .select, .co, .photo, .work, .yoga, .health, .fashion, and .surf among many others. 
**For this specific prize the domain must be one of those**

Your Validation Steps:
1.  **Validate TLD**: 
    * Analyze the URL string.
    * Ignore paths or protocols (e.g., `https://` or `/home`).
    * If it uses any other TLD (even valid ones like `.mx` or `.com`), it is **IMMEDIATELY DISQUALIFIED**.
2.  **Check Liveness**:
    * If the TLD is valid, use the `check_website_status` tool to ping the URL.
    * The site must be reachable (reachable: true) and return a success status code (200-299).
    * If the site returns 404, 500, or a connection error, it is considered "Inactive".

Output a SINGLE JSON object matching this schema:
{
  "domain_url": "string",
  "detected_tld": "string", 
  "is_active": true|false,
  "http_status": 200 | 404 | null,
  "final_determination": "QUALIFIED" | "DISQUALIFIED" | "NEEDS_MANUAL_REVIEW"
}

**Rules for Determination:**
* `has_tech_tld` is false -> DISQUALIFIED.
* `has_tech_tld` is true AND `is_active` is true -> QUALIFIED.
* `has_tech_tld` is true BUT `is_active` is false -> NEEDS_MANUAL_REVIEW.
"""
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