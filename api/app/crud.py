from sqlalchemy.orm import Session
from . import models, schemas

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_trend_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TrendItem).offset(skip).limit(limit).all()

def create_trend_item(db: Session, item: schemas.TrendItemCreate):
    db_item = models.TrendItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_ideas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Idea).offset(skip).limit(limit).all()

def create_idea(db: Session, idea: schemas.IdeaCreate):
    db_idea = models.Idea(**idea.dict())
    db.add(db_idea)
    db.commit()
    db.refresh(db_idea)
    return db_idea

def get_brand_profile(db: Session):
    return db.query(models.BrandProfile).first()

def create_or_update_brand_profile(db: Session, profile: schemas.BrandProfileCreate):
    db_profile = get_brand_profile(db)
    if db_profile:
        for key, value in profile.dict().items():
            setattr(db_profile, key, value)
    else:
        db_profile = models.BrandProfile(**profile.dict())
        db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

