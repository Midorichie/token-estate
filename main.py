# main.py enhancements
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from typing import List, Optional
import aiohttp
from decimal import Decimal
from datetime import datetime, timedelta

class MarketAnalysis(BaseModel):
    volume_24h: Decimal
    price_change_percentage: Decimal
    market_cap: Decimal
    liquidity_score: float
    predicted_price: Optional[Decimal]
    confidence_score: float

class BlockchainStatus(BaseModel):
    transaction_hash: str
    block_number: int
    confirmation_count: int
    status: str

@app.get("/market-analysis/{property_id}/enhanced", response_model=MarketAnalysis)
async def get_enhanced_market_analysis(
    property_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Get enhanced market analysis with predictions"""
    # Implementation connecting to Rust backend
    pass

@app.get("/properties/{property_id}/blockchain-status", response_model=BlockchainStatus)
async def get_blockchain_status(
    property_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Get blockchain registration status of a property"""
    pass

@app.post("/properties/{property_id}/verify")
async def verify_property_ownership(
    property_id: UUID,
    verification_data: PropertyVerificationData,
    current_user: User = Depends(get_current_user)
):
    """Verify property ownership through external sources"""
    pass

# blockchain_integration.py
from typing import Dict, Any
import aiohttp

class BlockchainService:
    def __init__(self, contract_address: str, network_url: str):
        self.contract_address = contract_address
        self.network_url = network_url
        
    async def submit_transaction(
        self,
        method: str,
        params: Dict[str, Any],
        wallet_credentials: Dict[str, str]
    ) -> str:
        """Submit transaction to blockchain"""
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                f"{self.network_url}/v2/transactions",
                json={
                    "contract_address": self.contract_address,
                    "method": method,
                    "params": params,
                    "wallet": wallet_credentials
                }
            )
            data = await response.json()
            return data["transaction_id"]
            
    async def get_property_tokens(
        self,
        property_id: int,
        holder_address: str
    ) -> int:
        """Get token balance for a property holder"""
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"{self.network_url}/v2/contracts/call-read",
                params={
                    "contract_address": self.contract_address,
                    "method": "get-token-balance",
                    "args": [str(property_id), holder_address]
                }
            )
            data = await response.json()
            return int(data["result"])

# security.py
from cryptography.fernet import Fernet
from jwt import encode, decode
from datetime import datetime, timedelta
from typing import Optional

class SecurityService:
    def __init__(self, encryption_key: bytes, jwt_secret: str):
        self.fernet = Fernet(encryption_key)
        self.jwt_secret = jwt_secret
        
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive property data"""
        return self.fernet.encrypt(data.encode()).decode()
        
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive property data"""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
        
    def generate_token(self, user_id: str) -> str:
        """Generate JWT token"""
        expiration = datetime.utcnow() + timedelta(days=1)
        return encode(
            {"sub": user_id, "exp": expiration},
            self.jwt_secret,
            algorithm="HS256"
        )