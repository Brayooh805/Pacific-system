from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional

# Import your custom files
from database import engine, SessionLocal, Base
from models import User, Product
import pdf_service  # This is the new file for generating PDFs

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS (Allows your HTML files to talk to this API) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- AUTHENTICATION SETUP ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Request Models (Data shapes coming from Frontend)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

class LoginRequest(BaseModel):
    email: str
    password: str

class ProductUpdateSchema(BaseModel):
    company_name: str
    rate_percent: float
    min_premium: int
    limit_windscreen: Optional[str] = "N/A"
    limit_entertainment: Optional[str] = "N/A"
    limit_towing: Optional[str] = "N/A"
    limit_repair: Optional[str] = "N/A"
    limit_medical: Optional[str] = "N/A"
    limit_tppd: Optional[str] = "N/A"
    excess_own_damage: Optional[str] = ""
    excess_theft_tracker: Optional[str] = ""
    excess_theft_no_tracker: Optional[str] = ""
    excess_young_driver: Optional[str] = ""
    pvt_status: Optional[str] = "Inclusive"

class QuoteRequest(BaseModel):
    client_name: str
    car_value: int
    reg_number: str       # Added
    make_model: str       # Added
    yom: int              # Added
    underwriter_name: str

# --- ENDPOINTS ---

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = pwd_context.hash(user.password)
    new_user = User(
        username=user.username, 
        email=user.email, 
        password_hash=hashed_pw, 
        role=user.role
    )
    db.add(new_user)
    db.commit()
    return {"msg": "User created successfully"}

@app.post("/login")
def login(creds: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or not pwd_context.verify(creds.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {
        "username": user.username, 
        "role": user.role, 
        "email": user.email
    }

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/admin/update-product")
def update_product(data: ProductUpdateSchema, db: Session = Depends(get_db)):
    # Check if company product exists
    product = db.query(Product).filter(Product.company_name == data.company_name).first()
    
    if not product:
        # Create new if it doesn't exist
        product = Product(company_name=data.company_name)
        db.add(product)
    
    # Update all fields
    product.rate_percent = data.rate_percent
    product.min_premium = data.min_premium
    product.limit_windscreen = data.limit_windscreen
    product.limit_entertainment = data.limit_entertainment
    product.limit_towing = data.limit_towing
    product.limit_repair = data.limit_repair
    product.limit_medical = data.limit_medical
    product.limit_tppd = data.limit_tppd
    product.excess_own_damage = data.excess_own_damage
    product.excess_theft_tracker = data.excess_theft_tracker
    product.excess_theft_no_tracker = data.excess_theft_no_tracker
    product.excess_young_driver = data.excess_young_driver
    product.pvt_status = data.pvt_status
    
    db.commit()
    return {"status": "success", "company": data.company_name}

@app.post("/generate-quote")
def generate_quote(request: QuoteRequest, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    
    if not products:
        raise HTTPException(status_code=404, detail="No products configured in Admin yet.")

    # Pass ALL the new details to the PDF service
    pdf_buffer = pdf_service.generate_pdf_buffer(
        client_name=request.client_name, 
        car_value=request.car_value, 
        reg_number=request.reg_number,   # New
        make_model=request.make_model,   # New
        yom=request.yom,                 # New
        underwriter_name=request.underwriter_name, 
        products=products
    )

    headers = {
        'Content-Disposition': f'attachment; filename="Quote_{request.client_name}.pdf"'
    }
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers) 

    # 3. Return the file
    headers = {
        'Content-Disposition': f'attachment; filename="Quote_{request.client_name}.pdf"'
    }
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)