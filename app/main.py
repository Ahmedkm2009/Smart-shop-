from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import products, ai

app = FastAPI(
    title=settings.app_name,
    description="AI-powered shopping backend. Uses FreeLLMAPI (or any OpenAI-compatible gateway) for recommendations and chat.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "llm_base_url": settings.openai_base_url,
        "llm_model": settings.llm_model,
    }


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "docs": "/docs",
        "health": "/health",
    }
