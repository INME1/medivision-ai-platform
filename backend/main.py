from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MediVision AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🏥 MediVision AI Platform API", "status": "running"}

@app.get("/health") 
def health():
    return {"status": "healthy"}

@app.post("/api/v1/auth/login")
def login():
    return {
        "access_token": "temporary_admin_token",
        "token_type": "bearer",
        "user": {"username": "admin", "name": "관리자"}
    }

@app.get("/api/v1/auth/me")
def get_me():
    return {"username": "admin", "name": "관리자"}
