from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
from . import crud, schemas
from .dependencies import get_db
from .auth import oauth_manager

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/x/login")
async def x_login(user_id: str = "demo-user"):
    """Initiate X (Twitter) OAuth login"""
    result = oauth_manager.get_x_auth_url(user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/x/callback")
async def x_callback(
    code: str = Query(...),
    state: str = Query(...),
    user_id: str = "demo-user",
    db: Session = Depends(get_db)
):
    """Handle X OAuth callback"""
    result = await oauth_manager.handle_x_callback(code, state, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Store the encrypted token in database
    account_data = schemas.AccountCreate(
        user_id=user_id,
        platform="x",
        oauth_json={"encrypted_token": result["encrypted_token"]}
    )
    
    # Check if account already exists
    existing_account = db.query(crud.models.Account).filter(
        crud.models.Account.user_id == user_id,
        crud.models.Account.platform == "x"
    ).first()
    
    if existing_account:
        existing_account.oauth_json = account_data.oauth_json
        db.commit()
        db.refresh(existing_account)
        account = existing_account
    else:
        account = crud.create_account(db, account_data)
    
    return {
        "message": "X authentication successful",
        "account_id": account.id,
        "platform": "x"
    }

@router.get("/instagram/login")
async def instagram_login(user_id: str = "demo-user"):
    """Initiate Instagram OAuth login"""
    result = oauth_manager.get_instagram_auth_url(user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/instagram/callback")
async def instagram_callback(
    code: str = Query(...),
    state: str = Query(...),
    user_id: str = "demo-user",
    db: Session = Depends(get_db)
):
    """Handle Instagram OAuth callback"""
    result = await oauth_manager.handle_instagram_callback(code, state, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Store the encrypted token in database
    account_data = schemas.AccountCreate(
        user_id=user_id,
        platform="instagram",
        oauth_json={"encrypted_token": result["encrypted_token"]}
    )
    
    # Check if account already exists
    existing_account = db.query(crud.models.Account).filter(
        crud.models.Account.user_id == user_id,
        crud.models.Account.platform == "instagram"
    ).first()
    
    if existing_account:
        existing_account.oauth_json = account_data.oauth_json
        db.commit()
        db.refresh(existing_account)
        account = existing_account
    else:
        account = crud.create_account(db, account_data)
    
    return {
        "message": "Instagram authentication successful",
        "account_id": account.id,
        "platform": "instagram"
    }

@router.get("/linkedin/login")
async def linkedin_login(user_id: str = "demo-user"):
    """Initiate LinkedIn OAuth login"""
    result = oauth_manager.get_linkedin_auth_url(user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/linkedin/callback")
async def linkedin_callback(
    code: str = Query(...),
    state: str = Query(...),
    user_id: str = "demo-user",
    db: Session = Depends(get_db)
):
    """Handle LinkedIn OAuth callback"""
    result = await oauth_manager.handle_linkedin_callback(code, state, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Store the encrypted token in database
    account_data = schemas.AccountCreate(
        user_id=user_id,
        platform="linkedin",
        oauth_json={"encrypted_token": result["encrypted_token"]}
    )
    
    # Check if account already exists
    existing_account = db.query(crud.models.Account).filter(
        crud.models.Account.user_id == user_id,
        crud.models.Account.platform == "linkedin"
    ).first()
    
    if existing_account:
        existing_account.oauth_json = account_data.oauth_json
        db.commit()
        db.refresh(existing_account)
        account = existing_account
    else:
        account = crud.create_account(db, account_data)
    
    return {
        "message": "LinkedIn authentication successful",
        "account_id": account.id,
        "platform": "linkedin"
    }

@router.get("/accounts")
async def get_connected_accounts(
    user_id: str = "demo-user",
    db: Session = Depends(get_db)
):
    """Get all connected accounts for a user"""
    accounts = db.query(crud.models.Account).filter(
        crud.models.Account.user_id == user_id
    ).all()
    
    account_list = []
    for account in accounts:
        account_list.append({
            "id": account.id,
            "platform": account.platform,
            "connected_at": account.created_at,
            "status": "connected"
        })
    
    return {"accounts": account_list}

@router.delete("/accounts/{account_id}")
async def disconnect_account(
    account_id: int,
    user_id: str = "demo-user",
    db: Session = Depends(get_db)
):
    """Disconnect a social media account"""
    account = db.query(crud.models.Account).filter(
        crud.models.Account.id == account_id,
        crud.models.Account.user_id == user_id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(account)
    db.commit()
    
    return {"message": f"{account.platform} account disconnected successfully"}
