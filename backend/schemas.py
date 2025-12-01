from pydantic import BaseModel
from typing import Optional

# --- USER SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"  # defaults to 'user', admin can change manually in DB if needed

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    role: str

# --- PRODUCT SCHEMAS ---
class ProductSchema(BaseModel):
    company_name: str
    
    # Financials
    rate_percent: float
    min_premium: int
    levies: Optional[str] = None
    
    # Limits (Box 2 on your PDF)
    limit_windscreen: Optional[str] = "N/A"
    limit_entertainment: Optional[str] = "N/A"
    limit_towing: Optional[str] = "N/A"
    limit_repair: Optional[str] = "N/A"
    limit_medical: Optional[str] = "N/A"
    limit_tppd: Optional[str] = "N/A"
    
    # Excesses (Box 3 on your PDF)
    excess_own_damage: Optional[str] = None
    excess_theft_tracker: Optional[str] = None
    excess_theft_no_tracker: Optional[str] = None
    excess_young_driver: Optional[str] = None
    
    pvt_status: Optional[str] = "Inclusive"