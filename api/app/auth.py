import os
import secrets
import hashlib
import base64
from typing import Dict, Any, Optional
from urllib.parse import urlencode, parse_qs
from authlib.integrations.httpx_client import AsyncOAuth2Client
from cryptography.fernet import Fernet
import json

class OAuthManager:
    """Manages OAuth flows for different social media platforms"""
    
    def __init__(self):
        self.state_secret = os.environ.get("OAUTH_STATE_SECRET", "change-me")
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for storing OAuth tokens"""
        key_file = "oauth_key.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key
    
    def encrypt_token(self, token_data: Dict[str, Any]) -> str:
        """Encrypt OAuth token data"""
        json_data = json.dumps(token_data)
        encrypted = self.cipher.encrypt(json_data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_token(self, encrypted_token: str) -> Dict[str, Any]:
        """Decrypt OAuth token data"""
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_token.encode())
            decrypted = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except Exception as e:
            print(f"Error decrypting token: {e}")
            return {}
    
    def generate_state(self, user_id: str, platform: str) -> str:
        """Generate secure state parameter for OAuth"""
        data = f"{user_id}:{platform}:{secrets.token_urlsafe(16)}"
        return hashlib.sha256(f"{data}:{self.state_secret}".encode()).hexdigest()
    
    def verify_state(self, state: str, user_id: str, platform: str) -> bool:
        """Verify OAuth state parameter"""
        # In a real implementation, store and verify state properly
        return len(state) == 64  # Simple check for demo
    
    # X (Twitter) OAuth
    def get_x_auth_url(self, user_id: str) -> Dict[str, str]:
        """Get X (Twitter) OAuth authorization URL"""
        client_id = os.environ.get("X_CLIENT_ID")
        redirect_uri = os.environ.get("X_REDIRECT_URI")
        
        if not client_id or not redirect_uri:
            return {"error": "X OAuth not configured"}
        
        state = self.generate_state(user_id, "x")
        
        # PKCE parameters
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode().rstrip('=')
        
        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": "tweet.read tweet.write users.read",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        }
        
        auth_url = f"https://twitter.com/i/oauth2/authorize?{urlencode(params)}"
        
        return {
            "auth_url": auth_url,
            "state": state,
            "code_verifier": code_verifier
        }
    
    async def handle_x_callback(self, code: str, state: str, user_id: str) -> Dict[str, Any]:
        """Handle X OAuth callback"""
        if not self.verify_state(state, user_id, "x"):
            return {"error": "Invalid state parameter"}
        
        # Mock successful token exchange
        mock_token_data = {
            "access_token": "mock_x_access_token",
            "refresh_token": "mock_x_refresh_token",
            "expires_in": 7200,
            "token_type": "bearer",
            "scope": "tweet.read tweet.write users.read"
        }
        
        encrypted_token = self.encrypt_token(mock_token_data)
        
        return {
            "success": True,
            "encrypted_token": encrypted_token,
            "platform": "x"
        }
    
    # Instagram OAuth
    def get_instagram_auth_url(self, user_id: str) -> Dict[str, str]:
        """Get Instagram OAuth authorization URL"""
        app_id = os.environ.get("FB_APP_ID")
        redirect_uri = os.environ.get("FB_REDIRECT_URI")
        
        if not app_id or not redirect_uri:
            return {"error": "Instagram OAuth not configured"}
        
        state = self.generate_state(user_id, "instagram")
        
        params = {
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "scope": "instagram_basic,instagram_content_publish",
            "response_type": "code",
            "state": state
        }
        
        auth_url = f"https://api.instagram.com/oauth/authorize?{urlencode(params)}"
        
        return {
            "auth_url": auth_url,
            "state": state
        }
    
    async def handle_instagram_callback(self, code: str, state: str, user_id: str) -> Dict[str, Any]:
        """Handle Instagram OAuth callback"""
        if not self.verify_state(state, user_id, "instagram"):
            return {"error": "Invalid state parameter"}
        
        # Mock successful token exchange
        mock_token_data = {
            "access_token": "mock_instagram_access_token",
            "user_id": "mock_instagram_user_id",
            "expires_in": 3600
        }
        
        encrypted_token = self.encrypt_token(mock_token_data)
        
        return {
            "success": True,
            "encrypted_token": encrypted_token,
            "platform": "instagram"
        }
    
    # LinkedIn OAuth
    def get_linkedin_auth_url(self, user_id: str) -> Dict[str, str]:
        """Get LinkedIn OAuth authorization URL"""
        client_id = os.environ.get("LINKEDIN_CLIENT_ID")
        redirect_uri = os.environ.get("LINKEDIN_REDIRECT_URI")
        
        if not client_id or not redirect_uri:
            return {"error": "LinkedIn OAuth not configured"}
        
        state = self.generate_state(user_id, "linkedin")
        
        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": "r_liteprofile r_emailaddress w_member_social",
            "state": state
        }
        
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
        
        return {
            "auth_url": auth_url,
            "state": state
        }
    
    async def handle_linkedin_callback(self, code: str, state: str, user_id: str) -> Dict[str, Any]:
        """Handle LinkedIn OAuth callback"""
        if not self.verify_state(state, user_id, "linkedin"):
            return {"error": "Invalid state parameter"}
        
        # Mock successful token exchange
        mock_token_data = {
            "access_token": "mock_linkedin_access_token",
            "expires_in": 5184000,  # 60 days
            "scope": "r_liteprofile r_emailaddress w_member_social"
        }
        
        encrypted_token = self.encrypt_token(mock_token_data)
        
        return {
            "success": True,
            "encrypted_token": encrypted_token,
            "platform": "linkedin"
        }
    
    def get_platform_token(self, encrypted_token: str) -> Optional[Dict[str, Any]]:
        """Get decrypted platform token"""
        return self.decrypt_token(encrypted_token)

# Global OAuth manager instance
oauth_manager = OAuthManager()
