# 🤖 Email AI System

Système intelligent de traitement automatique des emails basé sur les modèles de langage locaux (LLM).

## 📋 Description

Ce projet permet d'analyser automatiquement les emails entrants afin de :
- Détecter leur **catégorie** et **sous-catégorie**
- Extraire l'**intention principale** du message
- Générer automatiquement une **réponse professionnelle**

Le système fonctionne avec **Mistral** via **Ollama** — 100% local, sans API cloud.

## 🏗️ Architecture

```
email-ai-system/
├── app/
│   ├── main.py          # API REST FastAPI
│   ├── classifier.py    # Module de classification
│   ├── responder.py     # Module de génération de réponses
│   ├── llm_client.py    # Client Ollama
│   └── models.py        # Schémas Pydantic
├── data/
│   └── emails_sample.json  # Dataset de test
├── templates/
│   └── index.html       # Interface web
├── tests/
│   └── test_classifier.py  # Tests unitaires
├── evaluate.py          # Script d'évaluation
└── requirements.txt
```

## ⚙️ Installation

### Prérequis
- Python 3.11+
- [Ollama](https://ollama.ai)
- Mistral : `ollama pull mistral`

### Lancement

```bash
# 1. Cloner le repo
git clone https://github.com/elhathatefatine-rgb/email-ai-system.git
cd email-ai-system

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer Ollama
ollama serve

# 4. Lancer l'API
uvicorn app.main:app --reload
```

Ouvre **http://127.0.0.1:8000** dans ton navigateur.

## 📊 Performances

| Métrique | Score |
|---|---|
| Accuracy catégorie | **95%** |
| Accuracy sous-catégorie | **90%** |
| Tests unitaires | **6/6 ✅** |

## 🛠️ Stack technique

| Outil | Rôle |
|---|---|
| FastAPI | API REST |
| Ollama + Mistral | LLM local |
| Python 3.11 | Backend |
| Pytest | Tests unitaires |
| HTML/CSS/JS | Interface web |

## 📡 Endpoints API

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/health` | Statut de l'API |
| POST | `/classify` | Classifier un email |
| POST | `/respond` | Classifier + générer une réponse |

## 💡 Exemple d'utilisation

```bash
curl -X POST http://127.0.0.1:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"subject": "Commande non reçue", "body": "Ma commande n est pas arrivée."}'
```

Réponse :
```json
{
  "category": "Support client",
  "subcategory": "Suivi commande",
  "intent": "Signaler une commande non reçue",
  "priority": "high"
}
```

## 👩‍💻 Auteur

**Fatine Elhathat** — Stage 2026
