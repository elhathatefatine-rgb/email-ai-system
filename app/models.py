from pydantic import BaseModel

class EmailIn(BaseModel):
    subject: str
    body: str

class ClassificationResult(BaseModel):
    category: str
    subcategory: str
    intent: str
    priority: str

class EmailResponse(BaseModel):
    classification: dict
    suggested_response: str