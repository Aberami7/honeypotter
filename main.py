from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()

API_KEY = "mysecretkey"

@app.api_route("/honeypot", methods=["POST", "GET"])
async def honeypot(request: Request, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    scam_message = ""
    try:
        body = await request.json()
        scam_message = body.get("message", "")
    except:
        scam_message = ""

    is_scam = any(
        word in scam_message.lower()
        for word in ["urgent", "otp", "account", "upi", "blocked", "verify"]
    )

    return {
        "status": "success",
        "honeypot": "triggered",
        "is_scam": is_scam,
        "agent_reply": "Honeypot triggered"
    }


