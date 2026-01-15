"""
Updated Instagram Poster with Session Support
"""

import os
import json
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import HASHTAGS


class InstagramPoster:
    def __init__(self):
        self.client = Client()
        
        # Set device settings to look more legitimate
        self.client.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "OnePlus",
            "device": "devitron",
            "model": "6T Dev",
            "cpu": "qcom",
            "version_code": "314665256",
        })
        
        # Add delays to seem more human
        self.client.delay_range = [1, 3]
    
    def login(self):
        """
        Login using pre-created session (from your local machine)
        Falls back to username/password if no session
        """
        username = os.environ.get("IG_USERNAME")
        password = os.environ.get("IG_PASSWORD")
        session_data = os.environ.get("IG_SESSION")
        
        # Method 1: Use pre-created session (RECOMMENDED)
        if session_data:
            try:
                print("🔐 Attempting login with saved session...")
                session = json.loads(session_data)
                self.client.set_settings(session)
                self.client.login(username, password)
                
                # Verify session works
                self.client.get_timeline_feed()
                print("✅ Logged in using saved session!")
                return
                
            except Exception as e:
                print(f"⚠️ Session login failed: {e}")
                print("   Trying username/password...")
        
        # Method 2: Direct login (may fail on datacenter IPs)
        if not username or not password:
            raise ValueError(
                "Missing credentials! Set IG_USERNAME, IG_PASSWORD, "
                "and ideally IG_SESSION environment variables."
            )
        
        try:
            print("🔐 Attempting direct login...")
            self.client.login(username, password)
            print("✅ Direct login successful!")
            
        except Exception as e:
            raise Exception(
                f"Login failed: {e}\n\n"
                "💡 Solution: Create a session locally first!\n"
                "   Run create_session.py on your computer,\n"
                "   then add the session.json content as IG_SESSION secret."
            )
    
    def post(self, image_path: Path, caption: str) -> str:
        """Post image to Instagram"""
        self.login()
        
        # Add hashtags
        full_caption = f"{caption}\n\n{HASHTAGS}"
        
        # Upload
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
                    wait_time = (attempt + 1) * 60
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    raise


# === TEST LOCALLY ===
if __name__ == "__main__":
    poster = InstagramPoster()
    
    try:
        poster.login()
        print("✅ Login test successful!")
    except Exception as e:
        print(f"❌ Login test failed: {e}")