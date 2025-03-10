from fastapi import FastAPI
from database import engine, database
import models
from routers import user_router

app = FastAPI()

# Include routers
app.include_router(user_router.router)

# Startup and shutdown events for async database connection
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Create database tables
models.Base.metadata.create_all(bind=engine)
