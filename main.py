from fastapi import FastAPI, Header, Body
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

API_KEY = "mysecretkey"

@app.post("/honeypot")
async def honeypot(
    body: Optional[dict] = Body(default={}),
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "reply": None,
                "error": {
                    "message": "Invalid API Key",
                    "type": "AuthenticationError"
                }
            }
        )

    return {
        "status": "success",
        "reply": "Honeypot triggered",
        "error": None
    }
