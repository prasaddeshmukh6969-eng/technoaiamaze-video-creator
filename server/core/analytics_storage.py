"""
Simple JSON-based analytics storage system
Zero cost, perfect for validating demand before spending on paid services
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import threading

class AnalyticsStore:
    def __init__(self, file_path: str = "analytics_data.json"):
        self.file_path = Path(file_path)
        self.lock = threading.Lock()
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create analytics file with initial structure if it doesn't exist"""
        if not self.file_path.exists():
            initial_data = {
                "total_visitors": 0,
                "unique_visitors": set(),
                "page_views": {},
                "template_clicks": {
                    "restaurant": 0,
                    "real_estate": 0,
                    "education": 0,
                    "custom": 0
                },
                "emails": [],
                "feature_votes": {
                    "voice_cloning": 0,
                    "bulk_generation": 0,
                    "auto_resize": 0,
                    "custom_backgrounds": 0,
                    "scheduled_posts": 0
                },
                "events": []
            }
            self._write_data(initial_data)
    
    def _read_data(self) -> Dict:
        """Read analytics data from JSON file"""
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            # Convert unique_visitors list back to set
            if isinstance(data.get("unique_visitors"), list):
                data["unique_visitors"] = set(data["unique_visitors"])
            return data
    
    def _write_data(self, data: Dict):
        """Write analytics data to JSON file"""
        # Convert set to list for JSON serialization
        write_data = data.copy()
        if isinstance(write_data.get("unique_visitors"), set):
            write_data["unique_visitors"] = list(write_data["unique_visitors"])
        
        with open(self.file_path, 'w') as f:
            json.dump(write_data, f, indent=2)
    
    def track_page_view(self, page: str, visitor_id: str = None):
        """Track a page view"""
        with self.lock:
            data = self._read_data()
            
            # Increment total visitors
            data["total_visitors"] += 1
            
            # Track unique visitors
            if visitor_id:
                data["unique_visitors"].add(visitor_id)
            
            # Track page views
            if page not in data["page_views"]:
                data["page_views"][page] = 0
            data["page_views"][page] += 1
            
            # Add event
            data["events"].append({
                "type": "page_view",
                "page": page,
                "visitor_id": visitor_id,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 1000 events to prevent file from growing too large
            if len(data["events"]) > 1000:
                data["events"] = data["events"][-1000:]
            
            self._write_data(data)
    
    def track_template_click(self, template_id: str, visitor_id: str = None):
        """Track template card click"""
        with self.lock:
            data = self._read_data()
            
            # Increment template click count
            if template_id in data["template_clicks"]:
                data["template_clicks"][template_id] += 1
            
            # Add event
            data["events"].append({
                "type": "template_click",
                "template_id": template_id,
                "visitor_id": visitor_id,
                "timestamp": datetime.now().isoformat()
            })
            
            if len(data["events"]) > 1000:
                data["events"] = data["events"][-1000:]
            
            self._write_data(data)
    
    def add_email(self, email: str, source: str = "landing_page"):
        """Store email signup"""
        with self.lock:
            data = self._read_data()
            
            # Check if email already exists
            existing_emails = [e["email"] for e in data["emails"]]
            if email not in existing_emails:
                data["emails"].append({
                    "email": email,
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Add event
            data["events"].append({
                "type": "email_signup",
                "email": email,
                "source": source,
                "timestamp": datetime.now().isoformat()
            })
            
            if len(data["events"]) > 1000:
                data["events"] = data["events"][-1000:]
            
            self._write_data(data)
    
    def add_vote(self, feature_id: str, visitor_id: str = None):
        """Track feature vote"""
        with self.lock:
            data = self._read_data()
            
            # Increment vote count
            if feature_id in data["feature_votes"]:
                data["feature_votes"][feature_id] += 1
            
            # Add event
            data["events"].append({
                "type": "feature_vote",
                "feature_id": feature_id,
                "visitor_id": visitor_id,
                "timestamp": datetime.now().isoformat()
            })
            
            if len(data["events"]) > 1000:
                data["events"] = data["events"][-1000:]
            
            self._write_data(data)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get all analytics statistics"""
        with self.lock:
            data = self._read_data()
            
            # Calculate derived stats
            stats = {
                "total_visitors": data["total_visitors"],
                "unique_visitors": len(data["unique_visitors"]),
                "page_views": data["page_views"],
                "template_clicks": data["template_clicks"],
                "template_clicks_total": sum(data["template_clicks"].values()),
                "email_signups": len(data["emails"]),
                "emails": data["emails"],
                "feature_votes": data["feature_votes"],
                "feature_votes_total": sum(data["feature_votes"].values()),
                "recent_events": data["events"][-50:]  # Last 50 events
            }
            
            return stats
    
    def reset_stats(self):
        """Reset all analytics data (for testing)"""
        with self.lock:
            self.file_path.unlink(missing_ok=True)
            self._ensure_file_exists()

# Global instance
analytics_store = AnalyticsStore()
