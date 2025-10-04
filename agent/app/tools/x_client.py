import os
import httpx
from typing import Dict, List, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

class XClient:
    """X (Twitter) API client for trend scraping and posting"""
    
    def __init__(self):
        self.client_id = os.environ.get("X_CLIENT_ID")
        self.client_secret = os.environ.get("X_CLIENT_SECRET")
        self.base_url = "https://api.twitter.com/2"
        self.bearer_token = None
        
    async def authenticate(self) -> bool:
        """Authenticate with X API using OAuth2"""
        try:
            # In a real implementation, handle OAuth2 flow
            # For demo, return True if credentials exist
            return bool(self.client_id and self.client_secret)
        except Exception as e:
            print(f"X authentication error: {e}")
            return False
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def search_recent_tweets(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for recent tweets by query"""
        if not await self.authenticate():
            return []
            
        try:
            # Mock data for demo purposes
            mock_tweets = [
                {
                    "id": "1234567890",
                    "text": f"AI is transforming how we create content. The future is here! {query}",
                    "author_id": "user123",
                    "created_at": "2024-01-01T12:00:00Z",
                    "public_metrics": {
                        "retweet_count": 25,
                        "like_count": 150,
                        "reply_count": 10,
                        "quote_count": 5
                    },
                    "context_annotations": [
                        {"domain": {"name": "Technology"}, "entity": {"name": "Artificial Intelligence"}}
                    ]
                },
                {
                    "id": "1234567891",
                    "text": f"Content creators are leveraging AI tools for better engagement {query}",
                    "author_id": "user456",
                    "created_at": "2024-01-01T11:30:00Z",
                    "public_metrics": {
                        "retweet_count": 15,
                        "like_count": 89,
                        "reply_count": 7,
                        "quote_count": 3
                    }
                }
            ]
            
            return mock_tweets[:max_results]
            
        except Exception as e:
            print(f"Error searching tweets: {e}")
            return []
    
    async def get_trending_topics(self, woeid: int = 1) -> List[Dict[str, Any]]:
        """Get trending topics for a location"""
        try:
            # Mock trending topics
            mock_trends = [
                {
                    "name": "#AI",
                    "url": "https://twitter.com/search?q=%23AI",
                    "promoted_content": None,
                    "query": "%23AI",
                    "tweet_volume": 125000
                },
                {
                    "name": "#CreatorEconomy",
                    "url": "https://twitter.com/search?q=%23CreatorEconomy",
                    "promoted_content": None,
                    "query": "%23CreatorEconomy",
                    "tweet_volume": 45000
                },
                {
                    "name": "#SocialMedia",
                    "url": "https://twitter.com/search?q=%23SocialMedia",
                    "promoted_content": None,
                    "query": "%23SocialMedia",
                    "tweet_volume": 89000
                }
            ]
            
            return mock_trends
            
        except Exception as e:
            print(f"Error getting trending topics: {e}")
            return []
    
    async def post_tweet(self, text: str, media_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Post a tweet"""
        if not await self.authenticate():
            return {"error": "Authentication failed"}
            
        try:
            # Mock successful post
            return {
                "id": "1234567892",
                "text": text,
                "created_at": "2024-01-01T12:30:00Z",
                "author_id": "authenticated_user",
                "public_metrics": {
                    "retweet_count": 0,
                    "like_count": 0,
                    "reply_count": 0,
                    "quote_count": 0
                }
            }
            
        except Exception as e:
            print(f"Error posting tweet: {e}")
            return {"error": str(e)}
    
    def calculate_engagement_score(self, metrics: Dict[str, int]) -> float:
        """Calculate engagement score for a tweet"""
        likes = metrics.get("like_count", 0)
        retweets = metrics.get("retweet_count", 0)
        replies = metrics.get("reply_count", 0)
        quotes = metrics.get("quote_count", 0)
        
        # Weighted engagement score
        score = (likes * 1.0 + retweets * 2.0 + replies * 1.5 + quotes * 2.5) / 100
        return min(score, 1.0)  # Normalize to 0-1 range
