from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String) # "admin" or "user"

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True)
    company_color = Column(String, nullable=True) 
    
    # Financials
    rate_percent = Column(Float)
    min_premium = Column(Integer)
    levies = Column(String, nullable=True)
    
    # PDF Box Details
    limit_windscreen = Column(String, nullable=True)
    limit_entertainment = Column(String, nullable=True)
    limit_towing = Column(String, nullable=True)
    limit_repair = Column(String, nullable=True)
    limit_medical = Column(String, nullable=True)
    limit_tppd = Column(String, nullable=True)
    
    # Excesses
    excess_own_damage = Column(Text, nullable=True)
    excess_theft_tracker = Column(String, nullable=True)
    excess_theft_no_tracker = Column(String, nullable=True)
    excess_young_driver = Column(String, nullable=True)
    
    # The Missing Field
    pvt_status = Column(String, default="Inclusive")