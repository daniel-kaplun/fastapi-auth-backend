from fastapi import FastAPI

from app.routes.auth import router as auth_router

app = FastAPI(
    title="FastAPI Authentication Backend"
)

# Register authentication routes
app.include_router(auth_router)