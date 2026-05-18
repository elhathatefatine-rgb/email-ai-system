import json
import re
from app.llm_client import call_ollama

CLASSIFICATION_PROMPT = """Tu es un expert en classification d'emails professionnels en français.
Analyse attentivement cet email et retourne UNIQUEMENT un objet JSON valide.

RÈGLES IMPORTANTES :
- "Relance commerciale" = email qui RELANCE un devis/offre déjà envoyé
- "Demande de devis" = NOUVELLE demande de prix ou renouvellement de contrat
- "Réclamation" = produit reçu mais non conforme, endommagé ou mauvaise expérience
- "Remboursement" = demande EXPLICITE de remboursement d'argent
- "Question technique" = problème logiciel, connexion, application, bug
- "Question contrat" = questions sur clauses, attestations, documents RH

Catégories et sous-catégories STRICTES :
- Support client → Réclamation | Remboursement | Question technique | Suivi commande
- Commercial → Demande de devis | Partenariat | Relance commerciale
- RH → Candidature | Demande de congé | Question contrat
- Administratif → Facture | Contrat | Information générale

Format JSON attendu (rien d'autre) :
{{
  "category": "...",
  "subcategory": "...",
  "intent": "résumé de l'intention en français en une phrase",
  "priority": "high|medium|low"
}}

Email à analyser :
Sujet : {subject}
Corps : {body}

JSON :"""

async def classify_email(subject: str, body: str) -> dict:
    prompt = CLASSIFICATION_PROMPT.format(subject=subject, body=body)
    raw = await call_ollama(prompt)
    
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        match = re.search(r'\{.*?\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {
            "category": "Inconnu",
            "subcategory": "Inconnu",
            "intent": raw.strip()[:200],
            "priority": "medium"
        }