import spacy
import re

# Charger le modèle français
nlp = spacy.load("fr_core_news_sm")

# Mots urgents qui augmentent la priorité
URGENT_WORDS = [
    "urgent", "urgence", "immédiat", "immédiatement", "critique",
    "bloqué", "impossible", "grave", "sérieux", "emergency",
    "aujourd'hui", "maintenant", "rapidement", "vite", "asap"
]

# Mots négatifs pour détecter le sentiment
NEGATIVE_WORDS = [
    "insatisfait", "déçu", "problème", "erreur", "bug", "panne",
    "défectueux", "cassé", "abîmé", "endommagé", "manquant",
    "jamais", "aucun", "refus", "inacceptable", "honteux"
]

def preprocess_email(subject: str, body: str) -> dict:
    """
    Prétraitement NLP complet d'un email :
    - Nettoyage du texte
    - Tokenization
    - Suppression stopwords
    - Lemmatization
    - Détection urgence et sentiment
    """
    full_text = f"{subject} {body}"

    # 1. Nettoyage de base
    cleaned = clean_text(full_text)

    # 2. Traitement spaCy
    doc = nlp(cleaned)

    # 3. Tokens sans stopwords ni ponctuation
    tokens = [
        token.text.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and len(token.text) > 2
    ]

    # 4. Lemmatisation
    lemmas = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and len(token.text) > 2
    ]

    # 5. Entités nommées
    entities = [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
    ]

    # 6. Détection urgence
    text_lower = full_text.lower()
    is_urgent = any(word in text_lower for word in URGENT_WORDS)

    # 7. Détection sentiment négatif
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    sentiment = "négatif" if negative_count >= 2 else "neutre" if negative_count == 0 else "légèrement négatif"

    # 8. Calcul priorité enrichie
    priority = calculate_priority(is_urgent, negative_count)

    return {
        "cleaned_text": cleaned,
        "tokens": tokens[:20],       # Top 20 tokens
        "lemmas": lemmas[:20],        # Top 20 lemmes
        "entities": entities,
        "is_urgent": is_urgent,
        "sentiment": sentiment,
        "negative_score": negative_count,
        "suggested_priority": priority,
        "word_count": len(tokens)
    }

def clean_text(text: str) -> str:
    # Supprimer URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Supprimer emails
    text = re.sub(r'\S+@\S+', '', text)
    # Supprimer numéros de téléphone
    text = re.sub(r'\+?\d[\d\s\-\.]{8,}', '', text)
    # Supprimer caractères spéciaux excessifs
    text = re.sub(r'[^\w\s\-\'àâäéèêëîïôùûüçÀÂÄÉÈÊËÎÏÔÙÛÜÇ]', ' ', text)
    # Normaliser espaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_priority(is_urgent: bool, negative_count: int) -> str:
    if is_urgent or negative_count >= 3:
        return "high"
    elif negative_count >= 1:
        return "medium"
    else:
        return "low"