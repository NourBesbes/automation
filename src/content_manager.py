"""
Manages quote content from CSV file
"""

import pandas as pd
from datetime import datetime, date
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import QUOTES_CSV_PATH


class ContentManager:
    def __init__(self, csv_path: Path = QUOTES_CSV_PATH):
        self.csv_path = csv_path
        self.df = self._load_csv()
    
    def _load_csv(self) -> pd.DataFrame:
        """Load and validate CSV file"""
        df = pd.read_csv(self.csv_path)
        
        # Ensure required columns exist
        required_cols = ["date", "content"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV must contain columns: {required_cols}")
        
        # Parse dates
        df["date"] = pd.to_datetime(df["date"]).dt.date
        
        # Add posted column if not exists
        if "posted" not in df.columns:
            df["posted"] = False
        
        return df
    
    def get_today_quote(self) -> dict | None:
        """Get quote for today's date"""
        today = date.today()
        
        # First try: exact date match
        match = self.df[self.df["date"] == today]
        if not match.empty:
            row = match.iloc[0]
            return {
                "date": row["date"],
                "content": row["content"],
                "index": match.index[0]
            }
        
        # Second try: next unposted quote
        unposted = self.df[self.df["posted"] == False]
        if not unposted.empty:
            row = unposted.iloc[0]
            return {
                "date": today,  # Use today's date
                "content": row["content"],
                "index": unposted.index[0]
            }
        
        return None
    
    def mark_as_posted(self, index: int):
        """Mark a quote as posted and save CSV"""
        self.df.at[index, "posted"] = True
        self.df.at[index, "posted_date"] = datetime.now().isoformat()
        self.df.to_csv(self.csv_path, index=False)
        print(f"✅ Marked quote at index {index} as posted")
    
    def get_stats(self) -> dict:
        """Get posting statistics"""
        total = len(self.df)
        posted = self.df["posted"].sum()
        remaining = total - posted
        
        return {
            "total": total,
            "posted": posted,
            "remaining": remaining,
            "progress": f"{(posted/total)*100:.1f}%"
        }


# === QUICK TEST ===
if __name__ == "__main__":
    cm = ContentManager()
    
    print("📊 Stats:", cm.get_stats())
    print("📝 Today's quote:", cm.get_today_quote())