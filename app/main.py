from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models import EmailIn
from app.classifier import classify_email
from app.responder import generate_response
from app.database import create_tables, get_db, EmailAnalysis, EmailLog
import time

app = FastAPI(
    title="Email AI System",
    description="Système intelligent de traitement automatique des emails",
    version="2.0.0"
)

@app.on_event("startup")
async def startup():
    create_tables()
    print("Base de données initialisée ✅")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
async def health():
    return {"status": "ok", "message": "API opérationnelle", "version": "2.0.0"}

@app.post("/classify")
async def classify(email: EmailIn, db: Session = Depends(get_db)):
    try:
        start = time.time()
        result = await classify_email(email.subject, email.body)
        elapsed = round(time.time() - start, 2)

        log = EmailLog(endpoint="/classify", status="success")
        db.add(log)
        db.commit()

        result["processing_time"] = elapsed
        return result
    except Exception as e:
        log = EmailLog(endpoint="/classify", status="error", error_message=str(e))
        db.add(log)
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/respond")
async def respond(email: EmailIn, db: Session = Depends(get_db)):
    try:
        start = time.time()
        classification = await classify_email(email.subject, email.body)
        response = await generate_response(email.subject, email.body, classification)
        elapsed = round(time.time() - start, 2)

        # Sauvegarder dans la base de données
        analysis = EmailAnalysis(
            subject=email.subject,
            body=email.body,
            category=classification.get("category"),
            subcategory=classification.get("subcategory"),
            intent=classification.get("intent"),
            priority=classification.get("priority"),
            suggested_response=response,
            processing_time=elapsed
        )
        db.add(analysis)

        log = EmailLog(endpoint="/respond", status="success")
        db.add(log)
        db.commit()

        return {
            "classification": classification,
            "suggested_response": response,
            "processing_time": elapsed,
            "saved_id": analysis.id
        }
    except Exception as e:
        log = EmailLog(endpoint="/respond", status="error", error_message=str(e))
        db.add(log)
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(limit: int = 20, db: Session = Depends(get_db)):
    analyses = db.query(EmailAnalysis)\
        .order_by(EmailAnalysis.created_at.desc())\
        .limit(limit).all()
    return [
        {
            "id": a.id,
            "subject": a.subject,
            "category": a.category,
            "subcategory": a.subcategory,
            "priority": a.priority,
            "processing_time": a.processing_time,
            "created_at": str(a.created_at)
        }
        for a in analyses
    ]

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    total = db.query(EmailAnalysis).count()
    if total == 0:
        return {"total": 0, "message": "Aucun email analysé pour l'instant"}

    from sqlalchemy import func
    by_category = db.query(
        EmailAnalysis.category,
        func.count(EmailAnalysis.id).label("count")
    ).group_by(EmailAnalysis.category).all()

    by_priority = db.query(
        EmailAnalysis.priority,
        func.count(EmailAnalysis.id).label("count")
    ).group_by(EmailAnalysis.priority).all()

    avg_time = db.query(func.avg(EmailAnalysis.processing_time)).scalar()

    return {
        "total_emails": total,
        "by_category": {r.category: r.count for r in by_category},
        "by_priority": {r.priority: r.count for r in by_priority},
        "avg_processing_time": round(avg_time, 2) if avg_time else 0
    }

@app.delete("/history/{email_id}")
async def delete_analysis(email_id: int, db: Session = Depends(get_db)):
    analysis = db.query(EmailAnalysis).filter(EmailAnalysis.id == email_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Email non trouvé")
    db.delete(analysis)
    db.commit()
    return {"message": f"Email {email_id} supprimé"}