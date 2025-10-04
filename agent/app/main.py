from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from .simple_agent import generate_content_ideas

app = FastAPI(title="Social Agent Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateIdeasRequest(BaseModel):
    persona: str
    brand_rules: str
    platforms: List[str]
    ai_type: str = "text"

class RefreshTrendsRequest(BaseModel):
    topics: List[str] = ["#AI", "#CreatorEconomy", "#SocialMedia"]
    max_per_topic: int = 5

@app.get("/")
def read_root():
    return {"message": "Social Agent Service", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "agent"}

@app.post("/generate_ideas")
async def generate_ideas_endpoint(request: GenerateIdeasRequest):
    """Generate content ideas using LangGraph workflow"""
    try:
        result = generate_content_ideas(
            persona=request.persona,
            brand_rules=request.brand_rules,
            platforms=request.platforms
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh_trends")
async def refresh_trends_endpoint(request: RefreshTrendsRequest = None):
    """Refresh trending content from all platforms"""
    try:
        # Mock trends data for demo
        trends = [
            {
                "id": 1,
                "source": "linkedin",
                "topic": "#AI",
                "text": "AI agents are revolutionizing content creation workflows",
                "author": "TechInfluencer",
                "url": "https://linkedin.com/posts/tech-influencer-ai-agents",
                "engagement": {"likes": 150, "comments": 25, "shares": 30},
                "score": 0.85,
                "captured_at": "2024-01-01T12:00:00Z"
            },
            {
                "id": 2,
                "source": "x",
                "topic": "#CreatorEconomy",
                "text": "The creator economy is booming with new AI-powered tools",
                "author": "CreatorExpert",
                "url": "https://x.com/creatorexpert/status/1234567890",
                "engagement": {"likes": 200, "comments": 40, "shares": 50},
                "score": 0.92,
                "captured_at": "2024-01-01T11:30:00Z"
            },
            {
                "id": 3,
                "source": "instagram",
                "topic": "#SocialMedia",
                "text": "Social media strategies that actually work in 2024",
                "author": "SocialMediaGuru",
                "url": "https://instagram.com/p/socialmediaguru123",
                "engagement": {"likes": 300, "comments": 60, "shares": 25},
                "score": 0.78,
                "captured_at": "2024-01-01T10:15:00Z"
            }
        ]
        
        return {"trends": trends}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workflow_status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get the status of a running workflow"""
    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "progress": 100,
        "current_step": "scheduler_suggest",
        "results": {
            "ideas_generated": 2,
            "platforms_targeted": 3,
            "scheduled_posts": 6
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
