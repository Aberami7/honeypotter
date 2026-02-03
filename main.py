from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_KEY = "mysecretkey"

@app.post("/honeypot")
async def honeypot(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "status": "success",
        "message": "Honeypot triggered",
        "threat_level": "low"
    }

