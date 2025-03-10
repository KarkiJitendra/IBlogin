# main.py
from fastapi import FastAPI
from loginservice.api.routers import auth_router

app = FastAPI()

app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)