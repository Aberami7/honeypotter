from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

API_KEY = "mysecretkey"

class HoneypotRequest(BaseModel):
    message: Optional[str] = ""
    conversation_id: Optional[str] = "default"

@app.post("/honeypot")
def honeypot(
    request: HoneypotRequest = HoneypotRequest(),
    x_api_key: str = Header(..., alias="x-api-key")
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    scam_keywords = ["won", "prize", "lottery", "urgent", "upi", "account", "click"]

    is_scam = any(word in request.message.lower() for word in scam_keywords)

    agent_reply = (
        "Okay, I am interested. Please explain the next step."
        if is_scam
        else "Thanks for the information."
    )

    return {
        "is_scam": is_scam,
        "agent_reply": agent_reply,
        "extracted_intelligence": {
            "upi_id": "unknown",
            "bank_account": "unknown",
            "phishing_url": "unknown"
        },
        "status": "success"
    }
