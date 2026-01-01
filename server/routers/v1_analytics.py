"""
Analytics API endpoints
Track visitor behavior, template interest, email signups, and feature votes
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
from core.analytics_storage import analytics_store

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])

# Admin password from environment variable
ADMIN_PASSWORD = os.getenv("ANALYTICS_ADMIN_PASSWORD", "technoaiamaze2026")

# Request models
class PageViewEvent(BaseModel):
    page: str
    visitor_id: Optional[str] = None

class TemplateClickEvent(BaseModel):
    template_id: str
    visitor_id: Optional[str] = None

class EmailSignup(BaseModel):
    email: EmailStr
    source: str = "landing_page"

class FeatureVote(BaseModel):
    feature_id: str
    visitor_id: Optional[str] = None


@router.post("/page-view")
async def track_page_view(event: PageViewEvent):
    """Track a page view"""
    try:
        analytics_store.track_page_view(event.page, event.visitor_id)
        return {"status": "success", "message": "Page view tracked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/template-click")
async def track_template_click(event: TemplateClickEvent):
    """Track template card click"""
    try:
        analytics_store.track_template_click(event.template_id, event.visitor_id)
        return {"status": "success", "message": "Template click tracked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/email")
async def signup_email(signup: EmailSignup):
    """Store email signup"""
    try:
        analytics_store.add_email(signup.email, signup.source)
        return {
            "status": "success",
            "message": "Email signup successful! We'll notify you when we launch."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vote")
async def vote_feature(vote: FeatureVote):
    """Track feature vote"""
    try:
        analytics_store.add_vote(vote.feature_id, vote.visitor_id)
        return {"status": "success", "message": "Vote recorded! Thank you for your feedback."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats(password: Optional[str] = None):
    """
    Get analytics statistics (password protected)
    Usage: /api/v1/analytics/stats?password=YOUR_PASSWORD
    """
    if password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid password. Set ANALYTICS_ADMIN_PASSWORD environment variable."
        )
    
    try:
        stats = analytics_store.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_stats(password: Optional[str] = None):
    """
    Reset all analytics data (admin only, for testing)
    """
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    try:
        analytics_store.reset_stats()
        return {"status": "success", "message": "Analytics data reset"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
