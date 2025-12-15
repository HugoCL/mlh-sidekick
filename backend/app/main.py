import json
import re
import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import InMemoryRunner
from agents.gemini_agent import root_agent as gemini_checker_agent

app = FastAPI(
    title="MLH Sidekick API",
    description="Backend API for MLH Sidekick",
    version="0.1.0",
)
class HealthResponse(BaseModel):
    status: str
    message: str

class PrizeCheckRequest(BaseModel):
    repo_url: str
    project_number: str

def find_json_in_history(history):
    valid_json = None
    all_text = []
    for event in history:
        if hasattr(event, "content") and event.content and hasattr(event.content, "role"):
            if event.content.role == "model":
                for part in event.content.parts:
                    if part.text:
                        text = part.text
                        all_text.append(text)
                        json_block = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
                        if json_block:
                            try:
                                valid_json = json.loads(json_block.group(1))
                                continue
                            except: pass
                        raw_json = re.search(r"(\{.*\})", text, re.DOTALL)
                        if raw_json:
                            try:
                                valid_json = json.loads(raw_json.group(1))
                            except: pass
    if valid_json:
        return valid_json
    return {
        "final_determination": "NEEDS_MANUAL_REVIEW",
        "project_number_notes": "Agent failed to output valid JSON.",
        "raw_logs": all_text[-1] if all_text else "No response text found."
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to MLH Sidekick API"}

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="healthy", message="API is running")

@app.post("/api/agents/check-gemini-prize")
async def check_gemini_prize(request: PrizeCheckRequest):
    try:
        prompt = (
            f"Please check this project for the Gemini Prize.\n"
            f"GitHub Repository: {request.repo_url}\n"
            f"Submitted Project Number: {request.project_number}\n\n"
            f"SYSTEM INSTRUCTION: Do NOT explain your plan. Do NOT say 'I will start by...'. "
            f"Use the tools immediately. Output ONLY the final JSON object."
        )
        runner = InMemoryRunner(agent=gemini_checker_agent)
        history = await runner.run_debug(prompt, verbose=False)
        clean_result = find_json_in_history(history)
        
        return {"result": clean_result}
        
    except Exception as e:
        print(f"Error running agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))