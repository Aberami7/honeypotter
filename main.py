from fastapi import FastAPI, Header, HTTPException
from typing import Optional

app = FastAPI()

API_KEY = "mysecretkey"

@app.post("/honeypot")
def honeypot(
    message: str,
    conversation_id: Optional[str] = "default",
    x_api_key: str = Header(None)
):
    # API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Simple scam detection
    scam_keywords = ["won", "prize", "lottery", "urgent", "upi", "account", "click"]
    is_scam = any(word in message.lower() for word in scam_keywords)

    if is_scam:
        agent_reply = "Okay, I am interested. Please explain the next step."
    else:
        agent_reply = "Thanks for the information."

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
