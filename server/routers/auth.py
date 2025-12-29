"""
Authentication API Router
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

from ..core.auth_utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)
from ..core.user_storage import (
    create_user,
    get_user_by_email,
    get_user_by_id
)

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


# Request/Response Models
class RegisterRequest(BaseModel):
    email: EmailStr
    phone: str
    password: str
    
    @validator('phone')
    def validate_phone(cls, v):
        # Remove spaces and dashes
        phone = re.sub(r'[\s\-]', '', v)
        
        # Check if it's a valid phone number (basic validation)
        if not re.match(r'^\+?[1-9]\d{1,14}$', phone):
            raise ValueError('Invalid phone number format')
        
        return phone
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: str
    email: str
    phone: str
    created_at: str


# Authentication dependency
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Dependency to get current user from JWT token"""
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    # Verify token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user_id = payload.get("sub")
    user = get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not user.get('is_active'):
        raise HTTPException(status_code=401, detail="User account is disabled")
    
    return user


# Endpoints
@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    """Register a new user"""
    try:
        # Hash password
        password_hash = get_password_hash(request.password)
        
        # Create user
        user = create_user(
            email=request.email,
            phone=request.phone,
            password_hash=password_hash
        )
        
        # Create access token
        access_token = create_access_token(data={"sub": user['id']})
        
        # Remove sensitive data
        user_data = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login an existing user"""
    # Get user
    user = get_user_by_email(request.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Verify password
    if not verify_password(request.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Check if user is active
    if not user.get('is_active'):
        raise HTTPException(status_code=401, detail="User account is disabled")
    
    # Create access token
    access_token = create_access_token(data={"sub": user['id']})
    
    # Remove sensitive data
    user_data = {k: v for k, v in user.items() if k != 'password_hash'}
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user['id'],
        "email": current_user['email'],
        "phone": current_user['phone'],
        "created_at": current_user['created_at']
    }
