"""
Main orchestrator - ties everything together
"""

import sys
from pathlib import Path
from datetime import date

sys.path.append(str(Path(__file__).parent.parent))

from src.content_manager import ContentManager
from src.image_generator import ImageGenerator
from src.instagram_poster import InstagramPoster


def run_daily_post(dry_run: bool = False):
    """
    Main function to run daily posting workflow
    
    Args:
        dry_run: If True, generate image but don't post
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
    
    # Step 3: Post to Instagram
    if dry_run:
        print("\n🧪 Step 3: DRY RUN - Skipping Instagram post")
        print(f"   Image ready at: {image_path}")
    else:
        print("\n📱 Step 3: Posting to Instagram...")
        poster = InstagramPoster()
        
        caption = f"💡 {quote['content'][:100]}"
        poster.post_with_retry(image_path, caption)
        
        # Step 4: Mark as posted
        print("\n✏️  Step 4: Updating records...")
        content_mgr.mark_as_posted(quote["index"])
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ COMPLETED SUCCESSFULLY!")
    stats = content_mgr.get_stats()
    print(f"📊 Progress: {stats['posted']}/{stats['total']} posted ({stats['progress']})")
    print("=" * 50)
    
    return True


def test_pipeline():
    """Test the entire pipeline without posting"""
    print("🧪 Running pipeline test (dry run)...\n")
    run_daily_post(dry_run=True)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Instagram Automation")
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Generate image but don't post to Instagram"
    )
    parser.add_argument(
        "--test",
        action="store_true", 
        help="Run full pipeline test"
    )
    
    args = parser.parse_args()
    
    if args.test:
        test_pipeline()
    else:
        run_daily_post(dry_run=args.dry_run)