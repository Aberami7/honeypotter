from fastapi import FastAPI, Header, HTTPException, Body
from typing import Optional, Dict

app = FastAPI()

API_KEY = "mysecretkey"

@app.post("/honeypot")
async def honeypot(
    payload: Optional[Dict] = Body(default=None),
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "status": "success",
        "honeypot": "triggered",
        "is_scam": False,
        "agent_reply": "Honeypot triggered"
    }
