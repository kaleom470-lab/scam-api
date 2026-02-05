from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI()

API_KEY = "AbhiKey123"

security = HTTPBearer()

class InputData(BaseModel):
    conversation_id: str
    message: str
    history: list = []

def detect_scam(text):
    words = ["otp", "account", "urgent", "click", "verify", "upi", "bank"]
    return any(w in text.lower() for w in words)

@app.post("/scam-message")
async def scam_api(
    data: InputData,
    creds: HTTPAuthorizationCredentials = Depends(security)
):

    token = creds.credentials
    print("TOKEN RECEIVED:", token)

    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    scam = detect_scam(data.message)

    return {
        "scam_detected": scam,
        "agent_active": scam,
        "engagement_turns": len(data.history) + 1,
        "extracted_intelligence": {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_urls": []
        },
        "agent_reply": "Okay, please explain the steps."
    }