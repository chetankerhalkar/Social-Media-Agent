from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

from . import crud, models, schemas
from .database import SessionLocal, engine
from .dependencies import get_db
from .oauth_routes import router as oauth_router
from .agent_routes import router as agent_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Agent API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(oauth_router)
app.include_router(agent_router)

# Dependencies imported from dependencies.py

@app.get("/")
def read_root():
    return {"message": "Social Agent API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Trends endpoints
@app.post("/trends/refresh")
def refresh_trends(db: Session = Depends(get_db)):
    """Trigger trend scrapers"""
    # TODO: Implement trend scraping
    return {"message": "Trends refresh triggered"}

@app.get("/trends/list", response_model=List[schemas.TrendItem])
def list_trends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of trending items"""
    trends = crud.get_trend_items(db, skip=skip, limit=limit)
    return trends

# Ideas endpoints
@app.post("/ideas/generate")
def generate_ideas(
    persona: str,
    brand_rules: str,
    platforms: List[str],
    ai_type: str = "text",
    db: Session = Depends(get_db)
):
    """Generate content ideas using AI"""
    # TODO: Implement idea generation with LangGraph
    return {"message": "Ideas generation triggered", "platforms": platforms}

@app.get("/ideas/list", response_model=List[schemas.Idea])
def list_ideas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of ideas"""
    ideas = crud.get_ideas(db, skip=skip, limit=limit)
    return ideas

@app.get("/ideas/{idea_id}", response_model=schemas.Idea)
def get_idea(idea_id: int, db: Session = Depends(get_db)):
    """Get specific idea"""
    idea = db.query(models.Idea).filter(models.Idea.id == idea_id).first()
    if idea is None:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea

@app.post("/ideas/{idea_id}/approve")
def approve_idea(idea_id: int, db: Session = Depends(get_db)):
    """Approve an idea"""
    idea = db.query(models.Idea).filter(models.Idea.id == idea_id).first()
    if idea is None:
        raise HTTPException(status_code=404, detail="Idea not found")
    idea.status = "approved"
    db.commit()
    return {"message": "Idea approved"}

# Schedule endpoints
@app.post("/schedule/create")
def create_schedule(
    idea_id: int,
    platform: str,
    scheduled_for: str,
    timezone: str = "UTC",
    db: Session = Depends(get_db)
):
    """Schedule an idea for publishing"""
    # TODO: Implement scheduling logic
    return {"message": "Schedule created", "idea_id": idea_id, "platform": platform}

# Publishing endpoints
@app.post("/publish/run")
def run_publisher(db: Session = Depends(get_db)):
    """Manual run for due publishing jobs"""
    # TODO: Implement publishing logic
    return {"message": "Publisher run triggered"}

# Analytics endpoints
@app.post("/analytics/refresh")
def refresh_analytics(db: Session = Depends(get_db)):
    """Pull latest post metrics"""
    # TODO: Implement analytics refresh
    return {"message": "Analytics refresh triggered"}

# Brand profile endpoints
@app.get("/config/brand", response_model=schemas.BrandProfile)
def get_brand_config(db: Session = Depends(get_db)):
    """Get brand configuration"""
    profile = crud.get_brand_profile(db)
    if profile is None:
        # Return default profile
        return schemas.BrandProfile(
            id=0,
            persona="Playful AI coach for creators",
            brand_rules="Be optimistic, include actionable advice, keep it concise.",
            default_hashtags="#AI #CreatorEconomy"
        )
    return profile

@app.put("/config/brand", response_model=schemas.BrandProfile)
def update_brand_config(
    profile: schemas.BrandProfileCreate,
    db: Session = Depends(get_db)
):
    """Update brand configuration"""
    updated_profile = crud.create_or_update_brand_profile(db, profile)
    return updated_profile

# OAuth endpoints (placeholders)
@app.get("/auth/x/login")
def x_login():
    """X (Twitter) OAuth login"""
    return {"auth_url": "https://twitter.com/oauth/authorize"}

@app.get("/auth/x/callback")
def x_callback(code: str):
    """X (Twitter) OAuth callback"""
    return {"message": "X authentication successful"}

@app.get("/auth/instagram/login")
def instagram_login():
    """Instagram OAuth login"""
    return {"auth_url": "https://api.instagram.com/oauth/authorize"}

@app.get("/auth/instagram/callback")
def instagram_callback(code: str):
    """Instagram OAuth callback"""
    return {"message": "Instagram authentication successful"}

@app.get("/auth/linkedin/login")
def linkedin_login():
    """LinkedIn OAuth login"""
    return {"auth_url": "https://www.linkedin.com/oauth/v2/authorization"}

@app.get("/auth/linkedin/callback")
def linkedin_callback(code: str):
    """LinkedIn OAuth callback"""
    return {"message": "LinkedIn authentication successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
