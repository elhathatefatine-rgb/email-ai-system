import pytest
import asyncio
from app.classifier import classify_email

# Configuration pytest-asyncio
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

class TestClassifier:
    
    @pytest.mark.asyncio
    async def test_support_client_commande(self):
         result = await classify_email(
           subject="Ma commande n'est pas arrivée",
            body="Bonjour, ma commande numéro 12345 n'est pas arrivée depuis 3 semaines."
    )
         assert result["category"] == "Support client"
    # Suivi commande OU Réclamation sont tous les deux acceptables
         assert result["subcategory"] in ["Suivi commande", "Réclamation"]
         assert "priority" in result
         assert "intent" in result

    @pytest.mark.asyncio
    async def test_commercial_devis(self):
        result = await classify_email(
            subject="Demande de devis pour 10 licences",
            body="Bonjour, nous souhaitons acquérir 10 licences de votre logiciel. Merci de nous envoyer un devis."
        )
        assert result["category"] == "Commercial"
        assert result["subcategory"] == "Demande de devis"

    @pytest.mark.asyncio
    async def test_rh_candidature(self):
        result = await classify_email(
            subject="Candidature développeur Python",
            body="Bonjour, je souhaite postuler au poste de développeur Python. Veuillez trouver mon CV en pièce jointe."
        )
        assert result["category"] == "RH"
        assert result["subcategory"] == "Candidature"

    @pytest.mark.asyncio
    async def test_administratif_facture(self):
        result = await classify_email(
            subject="Facture impayée",
            body="Bonjour, la facture F-2026-001 d'un montant de 1500 euros est toujours impayée."
        )
        assert result["category"] == "Administratif"
        assert result["subcategory"] == "Facture"

    @pytest.mark.asyncio
    async def test_priority_high(self):
        result = await classify_email(
            subject="URGENT - Remboursement immédiat",
            body="Bonjour, j'exige un remboursement immédiat pour mon produit défectueux reçu hier."
        )
        assert result["priority"] == "high"

    @pytest.mark.asyncio
    async def test_result_structure(self):
        result = await classify_email(
            subject="Test structure",
            body="Ceci est un email de test pour vérifier la structure de la réponse."
        )
        assert "category" in result
        assert "subcategory" in result
        assert "intent" in result
        assert "priority" in result
        assert result["priority"] in ["high", "medium", "low"]