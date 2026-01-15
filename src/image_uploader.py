"""
Upload image to GitHub for hosting
Returns public URL for Graph API
"""

import os
import base64
import requests
from pathlib import Path
from datetime import datetime


class GitHubImageUploader:
    def __init__(self):
        self.token = os.environ.get("GH_TOKEN")
        self.repo = os.environ.get("GITHUB_REPOSITORY")  # Auto-set by GitHub Actions
        
        if not self.token:
            raise ValueError("Missing GH_TOKEN!")
    
    def upload(self, image_path: Path) -> str:
        """
        Upload image to GitHub repo and return raw URL
        
        Args:
            image_path: Local path to image
            
        Returns:
            Public URL of uploaded image
        """
        # Read image
        with open(image_path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"images/post_{timestamp}.png"
        
        # Upload via GitHub API
        url = f"https://api.github.com/repos/{self.repo}/contents/{filename}"
        
        response = requests.put(
            url,
            headers={
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            },
            json={
                "message": f"Upload image {timestamp}",
                "content": content
            }
        )
        
        if response.status_code not in [200, 201]:
            raise Exception(f"Upload failed: {response.text}")
        
        # Return raw URL
        raw_url = f"https://raw.githubusercontent.com/{self.repo}/main/{filename}"
        print(f"🖼️  Image uploaded: {raw_url}")
        
        return raw_url