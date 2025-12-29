"""
Backup script for users.json - creates encrypted backup to commit to GitHub
Run this periodically to backup user data
"""
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet

# Load or generate encryption key
KEY_FILE = Path(__file__).parent.parent / "data" / ".backup_key"
USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"
BACKUP_FILE = Path(__file__).parent.parent / "data" / "users_backup.enc"

def get_or_create_key():
    """Get existing key or create new one"""
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    else:
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
        print(f"✅ Created new encryption key: {KEY_FILE}")
        print("⚠️  IMPORTANT: Save this key securely! You'll need it to restore backups.")
        return key

def backup_users():
    """Create encrypted backup of users.json"""
    if not USERS_FILE.exists():
        print("❌ users.json not found!")
        return
    
    # Read users data
    users_data = USERS_FILE.read_bytes()
    
    # Encrypt
    key = get_or_create_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(users_data)
    
    # Save encrypted backup
    BACKUP_FILE.write_bytes(encrypted_data)
    
    print(f"✅ Backup created: {BACKUP_FILE}")
    print(f"📦 Size: {len(encrypted_data)} bytes")
    print(f"🔒 Encrypted with key from: {KEY_FILE}")

def restore_users():
    """Restore users.json from encrypted backup"""
    if not BACKUP_FILE.exists():
        print("❌ Backup file not found!")
        return
    
    if not KEY_FILE.exists():
        print("❌ Encryption key not found!")
        return
    
    # Read and decrypt
    encrypted_data = BACKUP_FILE.read_bytes()
    key = KEY_FILE.read_bytes()
    fernet = Fernet(key)
    
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Save to users.json
        USERS_FILE.write_bytes(decrypted_data)
        
        print(f"✅ Users restored from backup!")
        
    except Exception as e:
        print(f"❌ Decryption failed: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_users()
    else:
        backup_users()
