from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agent import agent_api

app = FastAPI()

class AgentRequest(BaseModel):
    prompt: str
    conversation_id: str
    user_name: str
    latitude: float
    longitude: float


@app.post("/agent")
def run_agent(request: AgentRequest):
    try:
        result = agent_api(
            prompt=request.prompt,
            conversation_id=request.conversation_id,
            user_name=request.user_name,
            latitude=request.latitude,
            longitude=request.longitude
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
