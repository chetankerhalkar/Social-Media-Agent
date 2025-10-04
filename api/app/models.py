from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    Float,
    ForeignKey,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    platform = Column(String, index=True)
    oauth_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TrendItem(Base):
    __tablename__ = "trend_items"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    topic = Column(String, index=True)
    url = Column(String, unique=True)
    author = Column(String)
    text = Column(Text)
    media_url = Column(String)
    like_count = Column(Integer, default=0)
    reshare_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    score = Column(Float, default=0.0)
    captured_at = Column(DateTime(timezone=True), server_default=func.now())
    raw_json = Column(JSON)


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    trend_id = Column(Integer, ForeignKey("trend_items.id"), nullable=True)
    title = Column(String)
    summary = Column(Text)
    persona = Column(Text)
    brand_rules = Column(Text)
    ai_type = Column(String, default="text")
    status = Column(String, default="draft", index=True)
    platform_targets = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    trend = relationship("TrendItem")
    assets = relationship("Asset", back_populates="idea")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))
    kind = Column(String)
    uri = Column(String)
    meta_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    idea = relationship("Idea", back_populates="assets")


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))
    platform = Column(String)
    scheduled_for = Column(DateTime(timezone=True))
    timezone = Column(String)
    status = Column(String, default="scheduled", index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    error = Column(Text, nullable=True)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))
    platform = Column(String)
    external_id = Column(String, unique=True)
    permalink = Column(String)
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    metrics_json = Column(JSON)


class MetricsSnapshot(Base):
    __tablename__ = "metrics_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    external_id = Column(String)
    snapshot_at = Column(DateTime(timezone=True), server_default=func.now())
    metrics_json = Column(JSON)


class BrandProfile(Base):
    __tablename__ = "brand_profile"

    id = Column(Integer, primary_key=True, index=True)
    persona = Column(Text)
    brand_rules = Column(Text)
    default_hashtags = Column(Text)
