from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.models import EmailIn
from app.classifier import classify_email
from app.responder import generate_response

app = FastAPI(
    title="Email AI System",
    description="Système intelligent de traitement automatique des emails",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
async def health():
    return {"status": "ok", "message": "API opérationnelle"}

@app.post("/classify")
async def classify(email: EmailIn):
    try:
        result = await classify_email(email.subject, email.body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/respond")
async def respond(email: EmailIn):
    try:
        classification = await classify_email(email.subject, email.body)
        response = await generate_response(email.subject, email.body, classification)
        return {
            "classification": classification,
            "suggested_response": response
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    