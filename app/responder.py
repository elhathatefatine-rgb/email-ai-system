from app.llm_client import call_ollama

RESPONSE_PROMPT = """Tu es un assistant professionnel chargé de rédiger des réponses d'emails.
Génère une réponse formelle, courtoise et adaptée à cet email.

Contexte de l'email :
- Catégorie : {category}
- Sous-catégorie : {subcategory}
- Intention : {intent}

Email original :
Sujet : {subject}
Corps : {body}

Rédige une réponse professionnelle en français (2-3 paragraphes, commence par "Bonjour,") :"""

async def generate_response(subject: str, body: str, classification: dict) -> str:
    prompt = RESPONSE_PROMPT.format(
        category=classification.get("category", ""),
        subcategory=classification.get("subcategory", ""),
        intent=classification.get("intent", ""),
        subject=subject,
        body=body
    )
    return await call_ollama(prompt)