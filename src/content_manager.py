"""
Manages quote content from CSV file
Support pour contenu arabe
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
        """Load and validate CSV file with Arabic content"""
        
        # Lire avec encodage UTF-8 pour l'arabe
        df = pd.read_csv(
            self.csv_path, 
            encoding='utf-8',
            dtype=str  # Tout en string d'abord
        )
        
        # Nettoyer les noms de colonnes
        df.columns = df.columns.str.strip().str.lower()
        
        # Vérifier colonnes requises
        required_cols = ["date", "content"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV doit contenir les colonnes: {required_cols}")
        
        # Parser les dates (format YYYY-MM-DD)
        df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d').dt.date
        
        # Nettoyer le contenu
        df["content"] = df["content"].str.strip()
        
        # Ajouter colonne posted si absente
        if "posted" not in df.columns:
            df["posted"] = False
        else:
            df["posted"] = df["posted"].fillna(False).astype(bool)
        
        return df
    
    def get_today_quote(self) -> dict | None:
        """Get quote for today's date"""
        today = date.today()
        
        # Premier essai: correspondance exacte de date
        match = self.df[self.df["date"] == today]
        if not match.empty:
            row = match.iloc[0]
            return {
                "date": row["date"],
                "content": row["content"],
                "index": match.index[0]
            }
        
        # Deuxième essai: prochaine citation non postée
        unposted = self.df[self.df["posted"] == False]
        if not unposted.empty:
            row = unposted.iloc[0]
            return {
                "date": row["date"],  # Utiliser la date du CSV
                "content": row["content"],
                "index": unposted.index[0]
            }
        
        return None
    
    def mark_as_posted(self, index: int):
        """Mark a quote as posted and save CSV"""
        self.df.at[index, "posted"] = True
        self.df.at[index, "posted_date"] = datetime.now().isoformat()
        
        # Sauvegarder avec encodage UTF-8
        self.df.to_csv(self.csv_path, index=False, encoding='utf-8')
        print(f"✅ Citation à l'index {index} marquée comme postée")
    
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


# === TEST ===
if __name__ == "__main__":
    cm = ContentManager()
    
    print("📊 Stats:", cm.get_stats())
    quote = cm.get_today_quote()
    if quote:
        print(f"📝 Citation du jour:")
        print(f"   Date: {quote['date']}")
        print(f"   Contenu: {quote['content'][:50]}...")