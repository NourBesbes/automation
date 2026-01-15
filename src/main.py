"""
Main orchestrator - Using Graph API
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
    Main function to run daily posting workflow
    """
    print("=" * 50)
    print("🚀 Instagram Automation Starting...")
    print("=" * 50)
    
    # Step 1: Get today's content
    print("\n📋 Step 1: Loading content...")
    content_mgr = ContentManager()
    quote = content_mgr.get_today_quote()
    
    if quote is None:
        print("❌ No content available for today!")
        print("💡 Add more quotes to your CSV file.")
        return False
    
    print(f"   Date: {quote['date']}")
    print(f"   Quote: {quote['content'][:50]}...")
    
    # Step 2: Generate image
    print("\n🎨 Step 2: Generating image...")
    generator = ImageGenerator()
    image_path = generator.generate(
        quote_text=quote["content"],
        quote_date=quote["date"]
    )
    
    if dry_run:
        print("\n🧪 DRY RUN - Skipping Instagram post")
        print(f"   Image ready at: {image_path}")
        return True
    
    # Step 3: Upload image to GitHub
    print("\n☁️  Step 3: Uploading image...")
    uploader = GitHubImageUploader()
    image_url = uploader.upload(image_path)
    
    # Step 4: Post to Instagram
    print("\n📱 Step 4: Posting to Instagram...")
    instagram = InstagramGraphAPI()
    
    caption = f"💡 {quote['content']}\n\n{HASHTAGS}"
    instagram.post_with_retry(image_url, caption)
    
    # Step 5: Mark as posted
    print("\n✏️  Step 5: Updating records...")
    content_mgr.mark_as_posted(quote["index"])
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ COMPLETED SUCCESSFULLY!")
    stats = content_mgr.get_stats()
    print(f"📊 Progress: {stats['posted']}/{stats['total']} posted ({stats['progress']})")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Instagram Automation")
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Generate image but don't post"
    )
    
    args = parser.parse_args()
    run_daily_post(dry_run=args.dry_run)