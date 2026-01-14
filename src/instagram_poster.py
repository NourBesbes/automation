"""
Handles Instagram authentication and posting
"""

import os
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import HASHTAGS


class InstagramPoster:
    def __init__(self):
        self.client = Client()
        self.session_file = Path(__file__).parent.parent / "session.json"
    
    def login(self):
        """
        Login to Instagram with session caching
        Uses environment variables for credentials
        """
        username = os.environ.get("IG_USERNAME")
        password = os.environ.get("IG_PASSWORD")
        
        if not username or not password:
            raise ValueError(
                "Missing credentials! Set IG_USERNAME and IG_PASSWORD "
                "environment variables."
            )
        
        # Try to load existing session
        if self.session_file.exists():
            try:
                self.client.load_settings(self.session_file)
                self.client.login(username, password)
                
                # Verify session is valid
                self.client.get_timeline_feed()
                print("✅ Logged in using cached session")
                return
                
            except LoginRequired:
                print("⚠️  Cached session expired, logging in fresh...")
                self.session_file.unlink()  # Delete old session
        
        # Fresh login
        self.client.login(username, password)
        self.client.dump_settings(self.session_file)
        print("✅ Fresh login successful, session cached")
    
    def post(self, image_path: Path, caption: str) -> str:
        """
        Post image to Instagram
        
        Args:
            image_path: Path to image file
            caption: Post caption
        
        Returns:
            Media ID of posted content
        """
        self.login()
        
        # Add hashtags to caption
        full_caption = f"{caption}\n\n{HASHTAGS}"
        
        # Upload photo
        media = self.client.photo_upload(
            path=str(image_path),
            caption=full_caption
        )
        
        print(f"🎉 Posted successfully! Media ID: {media.pk}")
        return media.pk
    
    def post_with_retry(self, image_path: Path, caption: str, 
                        max_retries: int = 3) -> str:
        """Post with automatic retry on failure"""
        import time
        
        for attempt in range(max_retries):
            try:
                return self.post(image_path, caption)
            
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 60  # 1min, 2min, 3min
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    raise


# === QUICK TEST ===
if __name__ == "__main__":
    # Test login only (don't actually post)
    poster = InstagramPoster()
    
    # Set these in your terminal first:
    # export IG_USERNAME="your_username"
    # export IG_PASSWORD="your_password"
    
    try:
        poster.login()
        print("✅ Login test successful!")
    except Exception as e:
        print(f"❌ Login test failed: {e}")