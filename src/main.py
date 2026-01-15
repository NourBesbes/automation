"""
Main orchestrator - Support Arabe
"""

import sys
from pathlib import Path
from datetime import date

sys.path.append(str(Path(__file__).parent.parent))

from src.content_manager import ContentManager
from src.image_generator import ImageGenerator
from src.instagram_graph_api import InstagramGraphAPI
from src.image_uploader import GitHubImageUploader
from config import HASHTAGS


def run_daily_post(dry_run: bool = False):
    """
    Main function pour publication quotidienne
    """
    print("=" * 50)
    print("🚀 Démarrage Automation Instagram...")
    print("=" * 50)
    
    # Étape 1: Charger le contenu
    print("\n📋 Étape 1: Chargement du contenu...")
    content_mgr = ContentManager()
    quote = content_mgr.get_today_quote()
    
    if quote is None:
        print("❌ Pas de contenu disponible!")
        print("💡 Ajoutez plus de citations dans votre CSV.")
        return False
    
    print(f"   Date: {quote['date']}")
    print(f"   Citation: {quote['content'][:50]}...")
    
    # Étape 2: Générer l'image
    print("\n🎨 Étape 2: Génération de l'image...")
    generator = ImageGenerator()
    image_path = generator.generate(
        quote_text=quote["content"],
        quote_date=quote["date"]
    )
    
    if dry_run:
        print("\n🧪 MODE TEST - Publication Instagram ignorée")
        print(f"   Image prête: {image_path}")
        return True
    
    # Étape 3: Upload de l'image
    print("\n☁️  Étape 3: Upload de l'image...")
    uploader = GitHubImageUploader()
    image_url = uploader.upload(image_path)
    
    # Étape 4: Publier sur Instagram
    print("\n📱 Étape 4: Publication sur Instagram...")
    instagram = InstagramGraphAPI()
    
    caption = f"💡 {quote['content']}\n\n{HASHTAGS}"
    instagram.post_with_retry(image_url, caption)
    
    # Étape 5: Marquer comme publié
    print("\n✏️  Étape 5: Mise à jour des enregistrements...")
    content_mgr.mark_as_posted(quote["index"])
    
    # Résumé
    print("\n" + "=" * 50)
    print("✅ TERMINÉ AVEC SUCCÈS!")
    stats = content_mgr.get_stats()
    print(f"📊 Progression: {stats['posted']}/{stats['total']} publiées ({stats['progress']})")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Instagram Automation Arabe")
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Générer l'image sans publier"
    )
    
    args = parser.parse_args()
    run_daily_post(dry_run=args.dry_run)