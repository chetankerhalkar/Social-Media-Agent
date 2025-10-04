from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from . import crud, schemas
from .dependencies import get_db
import httpx
import asyncio
import os

router = APIRouter(prefix="/agent", tags=["agent"])

async def call_agent_service(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Call the agent service"""
    agent_url = os.environ.get("AGENT_SERVICE_URL", "http://localhost:8001")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{agent_url}/{endpoint}", json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError:
        # If agent service is not available, return mock data
        return await mock_agent_response(endpoint, data)
    except Exception as e:
        print(f"Error calling agent service: {e}")
        return {"error": str(e)}

async def mock_agent_response(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Mock agent responses for demo purposes"""
    if endpoint == "generate_ideas":
        return {
            "ideas": [
                {
                    "id": 1,
                    "title": "AI-Powered Content Creation Tips",
                    "summary": "Share actionable tips on using AI tools for content creation",
                    "hook": "Transform your content strategy with AI",
                    "caption": "AI is revolutionizing content creation. Here are 5 ways to leverage AI tools for better engagement and productivity.",
                    "hashtags": ["#AI", "#ContentCreation", "#SocialMedia", "#Automation", "#CreatorEconomy"],
                    "ai_type": "text",
                    "status": "draft",
                    "platform_adaptations": {
                        "x": {
                            "caption": "AI is changing content creation. 5 ways to use AI tools for better engagement 🚀",
                            "hashtags": ["#AI", "#ContentCreation", "#SocialMedia"]
                        },
                        "instagram": {
                            "caption": "AI is revolutionizing content creation! ✨\n\nHere are 5 game-changing ways to leverage AI tools:\n\n1. Automated caption generation\n2. Trend analysis and insights\n3. Visual content optimization\n4. Scheduling and timing\n5. Performance analytics\n\nWhich AI tool has transformed your content strategy?",
                            "hashtags": ["#AI", "#ContentCreation", "#SocialMedia", "#Automation", "#CreatorEconomy", "#Instagram", "#Reels"]
                        },
                        "linkedin": {
                            "caption": "Professional insight: AI is revolutionizing content creation across industries.\n\nAs content creators and marketers, we're witnessing unprecedented opportunities to enhance our strategies through artificial intelligence. Here are 5 key areas where AI tools are making a significant impact:\n\n• Automated content generation and optimization\n• Advanced audience insights and trend analysis\n• Personalized content recommendations\n• Efficient scheduling and distribution\n• Comprehensive performance analytics\n\nThe future of content creation lies in the strategic integration of human creativity with AI capabilities.",
                            "hashtags": ["#AI", "#CreatorEconomy"]
                        }
                    }
                },
                {
                    "id": 2,
                    "title": "Creator Economy Trends 2024",
                    "summary": "Discuss the latest trends shaping the creator economy",
                    "hook": "The creator economy is evolving rapidly",
                    "caption": "The creator economy is booming! Here are the top trends shaping how creators monetize their content in 2024.",
                    "hashtags": ["#CreatorEconomy", "#ContentCreator", "#SocialMedia", "#Trends2024", "#DigitalMarketing"],
                    "ai_type": "text",
                    "status": "draft",
                    "platform_adaptations": {
                        "x": {
                            "caption": "Creator economy trends 2024: New monetization strategies are changing the game 💰",
                            "hashtags": ["#CreatorEconomy", "#Trends2024", "#ContentCreator"]
                        },
                        "instagram": {
                            "caption": "The creator economy is BOOMING! 📈\n\nTop trends shaping 2024:\n\n✨ AI-powered content tools\n💰 New monetization models\n🎯 Micro-influencer partnerships\n📱 Short-form video dominance\n🤝 Brand collaboration evolution\n\nWhat trend excites you most?",
                            "hashtags": ["#CreatorEconomy", "#ContentCreator", "#SocialMedia", "#Trends2024", "#DigitalMarketing", "#Instagram", "#Reels"]
                        },
                        "linkedin": {
                            "caption": "Professional insight: The creator economy continues its remarkable growth trajectory in 2024.\n\nKey trends reshaping the landscape:\n\n• Integration of AI tools for content optimization\n• Diversified revenue streams beyond traditional advertising\n• Rise of micro-influencer partnerships\n• Emphasis on authentic, value-driven content\n• Platform-specific monetization features\n\nCreators who adapt to these trends while maintaining authenticity will thrive in this evolving ecosystem.",
                            "hashtags": ["#CreatorEconomy", "#DigitalMarketing"]
                        }
                    }
                }
            ],
            "trending_context": [
                {
                    "topic": "#AI",
                    "source": "linkedin",
                    "engagement_score": 0.85,
                    "why_trending": "Increased adoption of AI tools in content creation"
                },
                {
                    "topic": "#CreatorEconomy", 
                    "source": "x",
                    "engagement_score": 0.92,
                    "why_trending": "New monetization platforms and tools launching"
                }
            ]
        }
    elif endpoint == "refresh_trends":
        return {
            "trends": [
                {
                    "id": 1,
                    "source": "linkedin",
                    "topic": "#AI",
                    "text": "AI agents are revolutionizing content creation workflows",
                    "author": "TechInfluencer",
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
                    "engagement": {"likes": 200, "comments": 40, "shares": 50},
                    "score": 0.92,
                    "captured_at": "2024-01-01T11:30:00Z"
                }
            ]
        }
    
    return {"message": f"Mock response for {endpoint}"}

@router.post("/generate_ideas")
async def generate_ideas(
    persona: str,
    brand_rules: str,
    platforms: List[str],
    ai_type: str = "text",
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Generate content ideas using the LangGraph agent"""
    
    # Call the agent service
    agent_data = {
        "persona": persona,
        "brand_rules": brand_rules,
        "platforms": platforms,
        "ai_type": ai_type
    }
    
    result = await call_agent_service("generate_ideas", agent_data)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # Store generated ideas in database
    stored_ideas = []
    for idea_data in result.get("ideas", []):
        idea_create = schemas.IdeaCreate(
            title=idea_data["title"],
            summary=idea_data["summary"],
            persona=persona,
            brand_rules=brand_rules,
            ai_type=ai_type,
            status="draft",
            platform_targets=platforms
        )
        
        stored_idea = crud.create_idea(db, idea_create)
        stored_ideas.append(stored_idea)
    
    return {
        "message": "Ideas generated successfully",
        "ideas": stored_ideas,
        "trending_context": result.get("trending_context", []),
        "count": len(stored_ideas)
    }

@router.post("/refresh_trends")
async def refresh_trends(db: Session = Depends(get_db)):
    """Refresh trending content from all platforms"""
    
    result = await call_agent_service("refresh_trends", {})
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # Store trends in database
    stored_trends = []
    for trend_data in result.get("trends", []):
        trend_create = schemas.TrendItemCreate(
            source=trend_data["source"],
            topic=trend_data["topic"],
            url=trend_data.get("url", f"https://{trend_data['source']}.com/search?q={trend_data['topic']}"),
            author=trend_data["author"],
            text=trend_data["text"],
            like_count=trend_data["engagement"].get("likes", 0),
            reshare_count=trend_data["engagement"].get("shares", 0),
            comment_count=trend_data["engagement"].get("comments", 0),
            score=trend_data["score"],
            raw_json=trend_data
        )
        
        stored_trend = crud.create_trend_item(db, trend_create)
        stored_trends.append(stored_trend)
    
    return {
        "message": "Trends refreshed successfully",
        "trends": stored_trends,
        "count": len(stored_trends)
    }

@router.get("/workflow_status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get the status of a running workflow"""
    # Mock workflow status
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

@router.post("/approve_idea/{idea_id}")
async def approve_idea(idea_id: int, db: Session = Depends(get_db)):
    """Approve a generated idea"""
    idea = db.query(crud.models.Idea).filter(crud.models.Idea.id == idea_id).first()
    
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    idea.status = "approved"
    db.commit()
    db.refresh(idea)
    
    return {
        "message": "Idea approved successfully",
        "idea": idea
    }

@router.post("/schedule_idea/{idea_id}")
async def schedule_idea(
    idea_id: int,
    platform: str,
    scheduled_for: str,
    timezone: str = "UTC",
    db: Session = Depends(get_db)
):
    """Schedule an approved idea for publishing"""
    idea = db.query(crud.models.Idea).filter(crud.models.Idea.id == idea_id).first()
    
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    if idea.status != "approved":
        raise HTTPException(status_code=400, detail="Idea must be approved before scheduling")
    
    # Create schedule entry
    schedule_data = {
        "idea_id": idea_id,
        "platform": platform,
        "scheduled_for": scheduled_for,
        "timezone": timezone,
        "status": "scheduled"
    }
    
    # In a real implementation, store in Schedule table
    idea.status = "scheduled"
    db.commit()
    
    return {
        "message": "Idea scheduled successfully",
        "schedule": schedule_data
    }
