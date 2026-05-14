"""TestApp - FastAPI Backend"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import hashlib
import secrets

app = FastAPI(
    title="TestApp API",
    description="Complete REST API for TestApp",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database
users_db = {}
items_db = []
user_id = 1
item_id = 1

# Models
class User(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    password: str

class Item(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_pw(plain: str, hashed: str) -> bool:
    return hash_pw(plain) == hashed

def new_token() -> str:
    return secrets.token_urlsafe(32)

# Routes
@app.get("/")
def root():
    return {"message": "TestApp API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "time": datetime.now().isoformat()}

@app.post("/register", status_code=201)
def register(user: User):
    global user_id
    if user.email in users_db:
        raise HTTPException(400, "Email exists")
    users_db[user.email] = {"id": user_id, "email": user.email, "name": user.name, "password": hash_pw(user.password)}
    user_id += 1
    return {"email": user.email, "name": user.name}

@app.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if not user or not verify_pw(form.password, user.get("password", "")):
        raise HTTPException(400, "Wrong credentials")
    return {"access_token": new_token(), "token_type": "bearer"}

@app.get("/items", response_model=List[Item])
def get_items():
    return items_db

@app.post("/items", response_model=Item)
def create_item(item: Item):
    global item_id
    item.id = item_id
    item_id += 1
    items_db.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(404, "Not found")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for i, existing in enumerate(items_db):
        if existing.id == item_id:
            item.id = item_id
            items_db[i] = item
            return item
    raise HTTPException(404, "Not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(i)
            return {"deleted": True}
    raise HTTPException(404, "Not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
