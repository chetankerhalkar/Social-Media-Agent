import os
import httpx
from typing import Dict, List, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

class InstagramClient:
    """Instagram Graph API client for content posting and analytics"""
    
    def __init__(self):
        self.app_id = os.environ.get("FB_APP_ID")
        self.app_secret = os.environ.get("FB_APP_SECRET")
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = None
        
    async def authenticate(self) -> bool:
        """Authenticate with Instagram Graph API"""
        try:
            # In a real implementation, handle OAuth flow
            return bool(self.app_id and self.app_secret)
        except Exception as e:
            print(f"Instagram authentication error: {e}")
            return False
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_hashtag_media(self, hashtag: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent media for a hashtag"""
        if not await self.authenticate():
            return []
            
        try:
            # Mock Instagram posts for demo
            mock_posts = [
                {
                    "id": "17841400008460056",
                    "media_type": "IMAGE",
                    "media_url": "https://example.com/image1.jpg",
                    "caption": f"Amazing content about {hashtag} #instagram #content",
                    "timestamp": "2024-01-01T12:00:00+0000",
                    "like_count": 245,
                    "comments_count": 18,
                    "permalink": "https://www.instagram.com/p/ABC123/"
                },
                {
                    "id": "17841400008460057",
                    "media_type": "VIDEO",
                    "media_url": "https://example.com/video1.mp4",
                    "caption": f"Check out this {hashtag} content! #reels #viral",
                    "timestamp": "2024-01-01T11:30:00+0000",
                    "like_count": 189,
                    "comments_count": 12,
                    "permalink": "https://www.instagram.com/p/DEF456/"
                }
            ]
            
            return mock_posts[:limit]
            
        except Exception as e:
            print(f"Error getting hashtag media: {e}")
            return []
    
    async def create_media_object(self, image_url: str, caption: str) -> Dict[str, Any]:
        """Create a media object for posting"""
        if not await self.authenticate():
            return {"error": "Authentication failed"}
            
        try:
            # Mock media object creation
            return {
                "id": "17841400008460058",
                "status": "FINISHED"
            }
            
        except Exception as e:
            print(f"Error creating media object: {e}")
            return {"error": str(e)}
    
    async def publish_media(self, creation_id: str) -> Dict[str, Any]:
        """Publish a created media object"""
        if not await self.authenticate():
            return {"error": "Authentication failed"}
            
        try:
            # Mock successful publication
            return {
                "id": "17841400008460059",
                "permalink": "https://www.instagram.com/p/GHI789/"
            }
            
        except Exception as e:
            print(f"Error publishing media: {e}")
            return {"error": str(e)}
    
    async def post_image(self, image_url: str, caption: str) -> Dict[str, Any]:
        """Post an image to Instagram"""
        # Create media object
        media_result = await self.create_media_object(image_url, caption)
        
        if "error" in media_result:
            return media_result
            
        # Publish the media
        return await self.publish_media(media_result["id"])
    
    async def get_account_insights(self, metrics: List[str]) -> Dict[str, Any]:
        """Get account insights/analytics"""
        if not await self.authenticate():
            return {"error": "Authentication failed"}
            
        try:
            # Mock insights data
            return {
                "data": [
                    {
                        "name": "impressions",
                        "period": "day",
                        "values": [{"value": 1250, "end_time": "2024-01-01T08:00:00+0000"}]
                    },
                    {
                        "name": "reach",
                        "period": "day", 
                        "values": [{"value": 980, "end_time": "2024-01-01T08:00:00+0000"}]
                    },
                    {
                        "name": "profile_views",
                        "period": "day",
                        "values": [{"value": 156, "end_time": "2024-01-01T08:00:00+0000"}]
                    }
                ]
            }
            
        except Exception as e:
            print(f"Error getting insights: {e}")
            return {"error": str(e)}
    
    def calculate_engagement_score(self, post_data: Dict[str, Any]) -> float:
        """Calculate engagement score for an Instagram post"""
        likes = post_data.get("like_count", 0)
        comments = post_data.get("comments_count", 0)
        
        # Simple engagement calculation
        # In real implementation, would include saves, shares, etc.
        total_engagement = likes + (comments * 3)  # Comments weighted more
        
        # Normalize based on typical Instagram engagement
        score = min(total_engagement / 1000, 1.0)
        return score
