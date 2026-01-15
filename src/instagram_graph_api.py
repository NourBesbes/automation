"""
Instagram Graph API Poster
Official API - Never blocked!
"""

import os
import requests
import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import HASHTAGS


class InstagramGraphAPI:
    def __init__(self):
        self.access_token = os.environ.get("IG_ACCESS_TOKEN")
        self.instagram_id = os.environ.get("IG_BUSINESS_ID")
        self.base_url = "https://graph.facebook.com/v18.0"
        
        if not self.access_token:
            raise ValueError("Missing IG_ACCESS_TOKEN!")
        if not self.instagram_id:
            raise ValueError("Missing IG_BUSINESS_ID!")
    
    def post_image(self, image_url: str, caption: str) -> str:
        """
        Post image to Instagram using Graph API
        
        Args:
            image_url: Public URL of the image (must be accessible online)
            caption: Post caption with hashtags
        
        Returns:
            Media ID of posted content
        """
        print("📤 Creating media container...")
        
        # Step 1: Create media container
        create_url = f"{self.base_url}/{self.instagram_id}/media"
        
        create_response = requests.post(create_url, data={
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        })
        
        if create_response.status_code != 200:
            raise Exception(f"Failed to create media: {create_response.text}")
        
        creation_id = create_response.json()["id"]
        print(f"✅ Media container created: {creation_id}")
        
        # Step 2: Wait for processing
        print("⏳ Waiting for Instagram to process image...")
        time.sleep(5)
        
        # Step 3: Publish the media
        print("📱 Publishing to Instagram...")
        publish_url = f"{self.base_url}/{self.instagram_id}/media_publish"
        
        publish_response = requests.post(publish_url, data={
            "creation_id": creation_id,
            "access_token": self.access_token
        })
        
        if publish_response.status_code != 200:
            raise Exception(f"Failed to publish: {publish_response.text}")
        
        media_id = publish_response.json()["id"]
        print(f"🎉 Posted successfully! Media ID: {media_id}")
        
        return media_id
    
    def post_with_retry(self, image_url: str, caption: str, 
                        max_retries: int = 3) -> str:
        """Post with automatic retry"""
        
        for attempt in range(max_retries):
            try:
                return self.post_image(image_url, caption)
                
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    raise


# === TEST ===
if __name__ == "__main__":
    api = InstagramGraphAPI()
    print(f"✅ Connected to Instagram ID: {api.instagram_id}")