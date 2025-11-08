from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from db import init_db, close_db  
from api import user_api 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up PULSE API...")
    await init_db()  
    yield
    print("🔄 Shutting down PULSE API...")
    await close_db()

# Wrapper Application
app = FastAPI(
    title="PULSE API Wrapper",
    lifespan=lifespan  
)

# Mount APIs
app.mount("/user_api", user_api)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)