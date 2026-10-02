from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import hashlib

app = FastAPI()
db = {}

class AuthPayload(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: AuthPayload):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=400, detail="Missing username or password")
    if payload.username in db:
        raise HTTPException(status_code=409, detail="User already exists")
    db[payload.username] = hashlib.sha256(payload.password.encode()).hexdigest()
    return {"message": "User registered successfully", "username": payload.username}

@app.post("/login", status_code=status.HTTP_200_OK)
def login(payload: AuthPayload):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=400, detail="Missing username or password")
    stored_hash = db.get(payload.username)
    if not stored_hash or stored_hash != hashlib.sha256(payload.password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "username": payload.username}
