"""
User storage and management - JSON file based
"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from threading import Lock

# File lock for thread-safe operations
_file_lock = Lock()

# Path to users database
USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"


def _read_users() -> List[Dict]:
    """Read users from JSON file"""
    if not USERS_FILE.exists():
        # Create file if it doesn't exist
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _write_users([])
        return []
    
    with _file_lock:
        try:
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
                return data.get('users', [])
        except json.JSONDecodeError:
            return []


def _write_users(users: List[Dict]) -> None:
    """Write users to JSON file"""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "users": users,
        "version": "1.0",
        "last_updated": datetime.utcnow().isoformat()
    }
    
    with _file_lock:
        with open(USERS_FILE, 'w') as f:
            json.dump(data, f, indent=2)


def create_user(email: str, phone: str, password_hash: str) -> Dict:
    """Create a new user"""
    users = _read_users()
    
    # Check if user already exists
    if any(u['email'] == email for u in users):
        raise ValueError("Email already registered")
    
    if any(u['phone'] == phone for u in users):
        raise ValueError("Phone number already registered")
    
    # Create new user
    new_user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "phone": phone,
        "password_hash": password_hash,
        "created_at": datetime.utcnow().isoformat(),
        "is_active": True
    }
    
    users.append(new_user)
    _write_users(users)
    
    return new_user


def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email"""
    users = _read_users()
    return next((u for u in users if u['email'] == email), None)


def get_user_by_id(user_id: str) -> Optional[Dict]:
    """Get user by ID"""
    users = _read_users()
    return next((u for u in users if u['id'] == user_id), None)


def get_user_by_phone(phone: str) -> Optional[Dict]:
    """Get user by phone"""
    users = _read_users()
    return next((u for u in users if u['phone'] == phone), None)


def update_user(user_id: str, updates: Dict) -> Optional[Dict]:
    """Update user information"""
    users = _read_users()
    
    for i, user in enumerate(users):
        if user['id'] == user_id:
            user.update(updates)
            user['updated_at'] = datetime.utcnow().isoformat()
            users[i] = user
            _write_users(users)
            return user
    
    return None


def get_all_users() -> List[Dict]:
    """Get all users (for admin purposes)"""
    return _read_users()
