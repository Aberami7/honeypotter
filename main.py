from fastapi import FastAPI, Header, HTTPException, Body
from typing import Optional

app = FastAPI()

API_KEY = "mysecretkey"

@app.post("/honeypot")
async def honeypot(
    body: Optional[dict] = Body(default={}),
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "status": "success",
        "honeypot": "triggered",
        "is_scam": False,
        "agent_reply": "Honeypot triggered"
    }
