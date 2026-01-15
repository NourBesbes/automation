# create_session.py
# Run this on YOUR computer (not GitHub!)

from instagrapi import Client
import json

def create_instagram_session():
    client = Client()
    
    # Your credentials (the NEW password you just created)
    username = "healyourlifewithfatmakrichen"
    password = "Maryambess8!"
    
    print("\n🔐 Logging in from your IP address...")
    
    try:
        client.login(username, password)
        print("✅ Login successful!")
        
        # Save session
        client.dump_settings("session.json")
        print("✅ Session saved to session.json")
        
        # Verify
        user_info = client.account_info()
        print(f"✅ Logged in as: {user_info.username}")
        
        print("\n" + "="*50)
        print("NEXT STEPS:")
        print("1. Copy session.json content")
        print("2. Add as GitHub Secret: IG_SESSION")
        print("="*50)
        
        # Print session for easy copy
        with open("session.json", "r") as f:
            session_data = f.read()
            print("\n📋 Session data (copy this):\n")
            print(session_data)
            
    except Exception as e:
        print(f"❌ Login failed: {e}")
        print("\n💡 Tips:")
        print("- Make sure you set a direct Instagram password")
        print("- Check if 2FA is enabled (disable it temporarily)")
        print("- Try logging into Instagram app first to verify password")

if __name__ == "__main__":
    create_instagram_session()