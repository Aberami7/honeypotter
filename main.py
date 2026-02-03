from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

API_KEY = "mysecretkey"

class HoneypotRequest(BaseModel):
    message: Optional[str] = None
    conversation_id: Optional[str] = None

@app.post("/honeypot")
def honeypot(
    request: Optional[HoneypotRequest] = None,
    x_api_key: str = Header(..., alias="x-api-key")
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    message = request.message if request and request.message else ""
    conversation_id = request.conversation_id if request and request.conversation_id else "default"

    scam_keywords = ["won", "prize", "lottery", "urgent", "upi", "account", "click"]
    is_scam = any(word in message.lower() for word in scam_keywords)

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
        "status": "success",
        "conversation_id": conversation_id
    }

