from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()
API_KEY = "mysecretkey"

@app.get("/")
def root():
    return {"status": "Honeypot API is live"}

@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str = Header(..., alias="x-api-key")
):
    if x_api_key.strip() != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        body = await request.json()
        message = body.get("message", "")
    except:
        message = ""

    is_scam = any(word in message.lower() for word in
                  ["urgent", "otp", "account", "upi", "verify", "blocked"])

    return {
        "status": "success",
        "honeypot": "triggered",
        "is_scam": is_scam,
        "agent_reply": "Honeypot triggered"
    }
