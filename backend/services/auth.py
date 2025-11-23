"""
Authentication service
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.schemas import User
from typing import Dict, Optional
import os


security = HTTPBearer(auto_error=False)
DEMO_MODE = os.getenv("DEMO_MODE", "0").lower() in {"1", "true", "yes"}


class AuthService:
    """Authentication and authorization service"""
    
    @staticmethod
    def verify_token(token: str) -> Dict:
        """Verify JWT token"""
        # In production, implement JWT verification
        return {
            "user_id": "demo_user_id",
            "email": "user@example.com"
        }


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> User:
    """
    Get current authenticated user from token
    In DEMO_MODE, returns a demo user without requiring authentication
    """
    # In DEMO_MODE, allow access without authentication
    if DEMO_MODE:
        return User(
            id="demo_user_id",
            email="demo@example.com",
            full_name="Demo User",
            role="user",
            created_at="2025-01-01T00:00:00Z"
        )
    
    # Production mode requires authentication
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        token = credentials.credentials
        payload = AuthService.verify_token(token)
        
        # In production, fetch user from database
        user = User(
            id=payload["user_id"],
            email=payload["email"],
            full_name="Demo User",
            role="user",
            created_at="2025-01-01T00:00:00Z"
        )
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
