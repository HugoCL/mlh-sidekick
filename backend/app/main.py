import json
import re
import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import InMemoryRunner
from agents.gemini_agent import root_agent
from agents.dot_tech_agent import tech_agent
from agents.mongodb_agent import root_agent as mongodb_agent
from agents.elevenlabs_agent import root_agent as elevenlabs_agent

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

class TechPrizeCheckRequest(BaseModel):
    project_url: str

class MongoDBPrizeCheckRequest(BaseModel):
    repo_url: str

class ElevenLabsPrizeCheckRequest(BaseModel):
    repo_url: str

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
        "notes": "Agent failed to output valid JSON.",
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
            f"SYSTEM INSTRUCTION: Do NOT explain your plan. Use the tools immediately. Output ONLY the final JSON object."
        )
        runner = InMemoryRunner(agent=root_agent)
        history = await runner.run_debug(prompt, verbose=False)
        clean_result = find_json_in_history(history)
        
        return {"result": clean_result}
        
    except Exception as e:
        print(f"Error running Gemini agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/check-dot-tech-prize")
async def check_dot_tech_prize(request: TechPrizeCheckRequest):
    try:
        prompt = (
            f"Please validate if this URL qualifies for the .Tech domain prize.\n"
            f"Project URL: {request.project_url}\n\n"
            f"Output ONLY the final JSON object."
        )
        
        # Initialize Runner with the Tech Agent
        runner = InMemoryRunner(agent=tech_agent)
        
        # Run the agent (async)
        history = await runner.run_debug(prompt, verbose=False)
        
        # Parse result
        clean_result = find_json_in_history(history)
        
        return {"result": clean_result}

    except Exception as e:
        print(f"Error running .Tech agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/check-mongodb-prize")
async def check_mongodb_prize(request: MongoDBPrizeCheckRequest):
    try:
        prompt = (
            f"Please check this project for the MongoDB Prize.\n"
            f"GitHub Repository: {request.repo_url}\n\n"
            f"SYSTEM INSTRUCTION: Do NOT explain your plan. Use the tools immediately. Output ONLY the final JSON object."
        )
        
        runner = InMemoryRunner(agent=mongodb_agent)
        history = await runner.run_debug(prompt, verbose=False)
        clean_result = find_json_in_history(history)
        
        return {"result": clean_result}
        
    except Exception as e:
        print(f"Error running MongoDB agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/check-elevenlabs-prize")
async def check_elevenlabs_prize(request: ElevenLabsPrizeCheckRequest):
    try:
        prompt = (
            f"Please check this project for the ElevenLabs Prize.\n"
            f"GitHub Repository: {request.repo_url}\n\n"
            f"SYSTEM INSTRUCTION: Do NOT explain your plan. Use the tools immediately. Output ONLY the final JSON object."
        )
        
        runner = InMemoryRunner(agent=elevenlabs_agent)
        history = await runner.run_debug(prompt, verbose=False)
        clean_result = find_json_in_history(history)
        
        return {"result": clean_result}
        
    except Exception as e:
        print(f"Error running ElevenLabs agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

