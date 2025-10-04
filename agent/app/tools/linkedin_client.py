import os
import asyncio
from typing import Dict, List, Any, Optional
from playwright.async_api import async_playwright
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
import random

class LinkedInClient:
    """LinkedIn client for web scraping and API integration"""
    
    def __init__(self):
        self.client_id = os.environ.get("LINKEDIN_CLIENT_ID")
        self.client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET")
        self.organization_urn = os.environ.get("LINKEDIN_ORGANIZATION_URN")
        self.api_base_url = os.environ.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")
        self.enable_public_scan = os.environ.get("ENABLE_LINKEDIN_PUBLIC", "true").lower() == "true"
        self.public_topics = os.environ.get("LINKEDIN_PUBLIC_TOPICS", "#AI,#CreatorEconomy").split(",")
        self.public_pages = os.environ.get("LINKEDIN_PUBLIC_PAGES", "").split(",")
        self.max_per_topic = int(os.environ.get("LINKEDIN_PUBLIC_MAX_PER_TOPIC", "5"))
        
    async def authenticate_api(self) -> bool:
        """Authenticate with LinkedIn Marketing API"""
        try:
            return bool(self.client_id and self.client_secret)
        except Exception as e:
            print(f"LinkedIn API authentication error: {e}")
            return False
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def scrape_public_posts(self, topic: str) -> List[Dict[str, Any]]:
        """Scrape public LinkedIn posts for a topic using Playwright"""
        if not self.enable_public_scan:
            return []
            
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = await context.new_page()
                
                # Search for the topic
                search_url = f"https://www.linkedin.com/search/results/content/?keywords={topic.replace('#', '%23')}"
                await page.goto(search_url, wait_until="networkidle")
                
                # Wait for content to load
                await page.wait_for_timeout(3000)
                
                # Mock scraped data for demo (in real implementation, parse actual content)
                mock_posts = [
                    {
                        "url": f"https://www.linkedin.com/posts/user1_{topic.replace('#', '')}_post1",
                        "author": "AI Expert",
                        "author_profile": "https://www.linkedin.com/in/ai-expert/",
                        "snippet": f"Exploring the latest trends in {topic}. The future of AI is bright!",
                        "engagement": {
                            "likes": random.randint(50, 500),
                            "comments": random.randint(5, 50),
                            "reposts": random.randint(2, 25)
                        },
                        "post_time": "2h ago",
                        "topic": topic
                    },
                    {
                        "url": f"https://www.linkedin.com/posts/user2_{topic.replace('#', '')}_post2",
                        "author": "Tech Innovator",
                        "author_profile": "https://www.linkedin.com/in/tech-innovator/",
                        "snippet": f"How {topic} is transforming business operations across industries",
                        "engagement": {
                            "likes": random.randint(100, 800),
                            "comments": random.randint(10, 80),
                            "reposts": random.randint(5, 40)
                        },
                        "post_time": "4h ago",
                        "topic": topic
                    }
                ]
                
                await browser.close()
                return mock_posts[:self.max_per_topic]
                
        except Exception as e:
            print(f"Error scraping LinkedIn posts for {topic}: {e}")
            return []
    
    async def scrape_company_posts(self, company_url: str) -> List[Dict[str, Any]]:
        """Scrape posts from a specific company page"""
        if not self.enable_public_scan:
            return []
            
        try:
            # Mock company posts for demo
            mock_posts = [
                {
                    "url": f"{company_url}/posts/company_post_1",
                    "author": "Company Official",
                    "snippet": "Exciting updates from our AI research team!",
                    "engagement": {
                        "likes": random.randint(200, 1000),
                        "comments": random.randint(20, 100),
                        "reposts": random.randint(10, 50)
                    },
                    "post_time": "1d ago",
                    "company_url": company_url
                }
            ]
            
            return mock_posts
            
        except Exception as e:
            print(f"Error scraping company posts from {company_url}: {e}")
            return []
    
    async def get_trending_topics(self) -> Dict[str, Any]:
        """Get trending topics from LinkedIn"""
        topics_data = {"topics": []}
        
        for topic in self.public_topics:
            topic = topic.strip()
            posts = await self.scrape_public_posts(topic)
            
            if posts:
                # Calculate topic score
                total_engagement = sum(
                    post["engagement"]["likes"] + 
                    post["engagement"]["comments"] * 2 + 
                    post["engagement"]["reposts"] * 3
                    for post in posts
                )
                
                avg_score = total_engagement / len(posts) / 1000  # Normalize
                
                topic_data = {
                    "name": topic,
                    "posts": posts,
                    "why_now": f"{topic} is trending due to increased engagement and industry adoption",
                    "idea_seeds": [
                        f"Create educational content about {topic}",
                        f"Share case studies related to {topic}",
                        f"Discuss future implications of {topic}"
                    ],
                    "score": min(avg_score, 1.0)
                }
                
                topics_data["topics"].append(topic_data)
        
        # Sort by score
        topics_data["topics"].sort(key=lambda x: x["score"], reverse=True)
        
        return topics_data
    
    async def post_to_linkedin(self, content: str, organization_id: Optional[str] = None) -> Dict[str, Any]:
        """Post content to LinkedIn (requires API authentication)"""
        if not await self.authenticate_api():
            return {"error": "API authentication failed"}
            
        try:
            # Mock successful post
            return {
                "id": "urn:li:share:1234567890",
                "permalink": "https://www.linkedin.com/posts/activity-1234567890",
                "created_at": "2024-01-01T12:00:00Z"
            }
            
        except Exception as e:
            print(f"Error posting to LinkedIn: {e}")
            return {"error": str(e)}
    
    async def get_organization_analytics(self) -> Dict[str, Any]:
        """Get organization analytics from LinkedIn Marketing API"""
        if not await self.authenticate_api():
            return {"error": "API authentication failed"}
            
        try:
            # Mock analytics data
            return {
                "data": [
                    {
                        "metric": "impressions",
                        "value": 15000,
                        "period": "last_30_days"
                    },
                    {
                        "metric": "clicks",
                        "value": 1200,
                        "period": "last_30_days"
                    },
                    {
                        "metric": "engagement_rate",
                        "value": 0.08,
                        "period": "last_30_days"
                    }
                ]
            }
            
        except Exception as e:
            print(f"Error getting LinkedIn analytics: {e}")
            return {"error": str(e)}
    
    def calculate_engagement_score(self, post_data: Dict[str, Any]) -> float:
        """Calculate engagement score for a LinkedIn post"""
        engagement = post_data.get("engagement", {})
        likes = engagement.get("likes", 0)
        comments = engagement.get("comments", 0)
        reposts = engagement.get("reposts", 0)
        
        # LinkedIn engagement scoring
        score = (likes * 1.0 + comments * 3.0 + reposts * 2.0) / 500
        return min(score, 1.0)
