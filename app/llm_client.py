import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral"

async def call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    try:
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(OLLAMA_URL, json={
                "model": model,
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()
            return response.json()["response"]
    except httpx.ConnectError:
        raise Exception("Ollama n'est pas lancé. Exécute 'ollama serve' dans un terminal.")
    except httpx.ReadTimeout:
        raise Exception("Timeout : Mistral met trop de temps. Réessaie avec un texte plus court.")
    except Exception as e:
        raise Exception(f"Erreur LLM : {str(e)}")