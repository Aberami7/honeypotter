from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()

API_KEY = "mysecretkey"

@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str | None = Header(None, alias="x-api-key")
):
    # Manual API key check (prevents 422)
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Safe body parsing
    try:
        body = await request.json()
    except:
        body = {}

    message = ""
    conversation_id = "default"

    if isinstance(body, dict):
        message = body.get("message", "")
        conversation_id = body.get("conversation_id", "default")

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


@app.get("/honeypot")
def honeypot_info():
    return {
        "message": "POST endpoint. Send x-api-key header and optional JSON body."
    }
