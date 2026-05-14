from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="My API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

items_db: List[Item] = []
item_id = 1

@app.get("/")
def root():
    return {"message": "My API", "version": "1.0.0"}

@app.get("/items")
def get_items():
    return items_db

@app.post("/items")
def create_item(item: Item):
    global item_id
    item.id = item_id
    item_id += 1
    items_db.append(item)
    return item

@app.get("/health")
def health():
    return {"status": "healthy"}
