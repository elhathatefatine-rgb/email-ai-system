import asyncio
import json
from app.classifier import classify_email

async def evaluate():
    # Charger le dataset
    with open("data/emails_sample.json", "r", encoding="utf-8") as f:
        emails = json.load(f)

    correct_category = 0
    correct_subcategory = 0
    total = len(emails)
    results = []

    print(f"\n{'='*60}")
    print(f"  ÉVALUATION DU SYSTÈME - {total} emails")
    print(f"{'='*60}\n")

    for email in emails:
        print(f"Test {email['id']} : {email['subject'][:40]}...")
        
        result = await classify_email(email["subject"], email["body"])
        
        cat_ok = result.get("category") == email["expected_category"]
        sub_ok = result.get("subcategory") == email["expected_subcategory"]
        
        if cat_ok:
            correct_category += 1
        if sub_ok:
            correct_subcategory += 1

        status = "✅" if cat_ok else "❌"
        print(f"  {status} Catégorie : {result.get('category')} (attendu: {email['expected_category']})")
        print(f"  {'✅' if sub_ok else '❌'} Sous-cat  : {result.get('subcategory')} (attendu: {email['expected_subcategory']})")
        print()

        results.append({
            "id": email["id"],
            "subject": email["subject"],
            "expected_category": email["expected_category"],
            "predicted_category": result.get("category"),
            "category_correct": cat_ok,
            "expected_subcategory": email["expected_subcategory"],
            "predicted_subcategory": result.get("subcategory"),
            "subcategory_correct": sub_ok
        })

    # Résultats finaux
    acc_cat = (correct_category / total) * 100
    acc_sub = (correct_subcategory / total) * 100

    print(f"{'='*60}")
    print(f"  RÉSULTATS FINAUX")
    print(f"{'='*60}")
    print(f"  Accuracy catégorie    : {correct_category}/{total} = {acc_cat:.1f}%")
    print(f"  Accuracy sous-cat     : {correct_subcategory}/{total} = {acc_sub:.1f}%")
    print(f"{'='*60}\n")

    # Sauvegarder les résultats
    with open("data/evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "accuracy_category": acc_cat,
            "accuracy_subcategory": acc_sub,
            "details": results
        }, f, ensure_ascii=False, indent=2)

    print("Résultats sauvegardés dans data/evaluation_results.json")

if __name__ == "__main__":
    asyncio.run(evaluate())