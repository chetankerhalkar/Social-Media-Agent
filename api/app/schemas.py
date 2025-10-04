from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class AccountBase(BaseModel):
    user_id: str
    platform: str

class AccountCreate(AccountBase):
    oauth_json: Dict[str, Any]

class Account(AccountBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TrendItemBase(BaseModel):
    source: str
    topic: str
    url: str
    author: str
    text: str
    media_url: Optional[str] = None
    like_count: int = 0
    reshare_count: int = 0
    comment_count: int = 0
    score: float = 0.0

class TrendItemCreate(TrendItemBase):
    raw_json: Dict[str, Any]

class TrendItem(TrendItemBase):
    id: int
    captured_at: datetime

    class Config:
        from_attributes = True

class IdeaBase(BaseModel):
    title: str
    summary: str
    persona: str
    brand_rules: str
    ai_type: str = "text"
    status: str = "draft"
    platform_targets: List[str]

class IdeaCreate(IdeaBase):
    trend_id: Optional[int] = None

class Idea(IdeaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AssetBase(BaseModel):
    idea_id: int
    kind: str
    uri: str

class AssetCreate(AssetBase):
    meta_json: Optional[Dict[str, Any]] = None

class Asset(AssetBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ScheduleBase(BaseModel):
    idea_id: int
    platform: str
    scheduled_for: datetime
    timezone: str

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    status: str
    post_id: Optional[int] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    idea_id: int
    platform: str
    external_id: str
    permalink: str

class PostCreate(PostBase):
    metrics_json: Optional[Dict[str, Any]] = None

class Post(PostBase):
    id: int
    posted_at: datetime

    class Config:
        from_attributes = True

class BrandProfileBase(BaseModel):
    persona: str
    brand_rules: str
    default_hashtags: Optional[str] = None

class BrandProfileCreate(BrandProfileBase):
    pass

class BrandProfile(BrandProfileBase):
    id: int

    class Config:
        from_attributes = True

