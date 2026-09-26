from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.routers.products import _products
from app.services.llm import chat

router = APIRouter(prefix="/ai", tags=["ai"])


class RecommendRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    max_items: int = Field(3, ge=1, le=10)


class RecommendResponse(BaseModel):
    recommendation: str
    matched_products: list[dict]


@router.post("/recommend", response_model=RecommendResponse)
async def recommend_products(payload: RecommendRequest):
    """Use FreeLLMAPI to recommend products based on a natural-language query."""
    if not _products:
        raise HTTPException(
            status_code=400,
            detail="No products in catalog yet. Add some products first.",
        )

    catalog = "\n".join(
        f"- ID {p['id']}: {p['name']} (${p['price']}) — {p['description'] or 'no description'} [stock: {p['stock']}]"
        for p in _products.values()
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful shopping assistant for Smart-shop-. "
                "Recommend the most relevant products from the catalog based on the user query. "
                "Be concise and friendly. Mention product names and why they fit."
            ),
        },
        {
            "role": "user",
            "content": f"Catalog:\n{catalog}\n\nUser query: {payload.query}\n\nRecommend up to {payload.max_items} products.",
        },
    ]

    try:
        recommendation = await chat(messages)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"LLM gateway error: {e!s}. Check OPENAI_API_KEY and OPENAI_BASE_URL (FreeLLMAPI).",
        ) from e

    # Simple keyword match for matched_products (MVP)
    query_lower = payload.query.lower()
    matched = [
        p
        for p in _products.values()
        if any(
            word in p["name"].lower() or word in (p["description"] or "").lower()
            for word in query_lower.split()
            if len(word) > 2
        )
    ][: payload.max_items]

    return RecommendResponse(
        recommendation=recommendation,
        matched_products=matched,
    )


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


@router.post("/chat")
async def ai_chat(payload: ChatRequest):
    """General shopping assistant chat via FreeLLMAPI."""
    messages = [
        {
            "role": "system",
            "content": "You are a friendly AI shopping assistant for Smart-shop-. Help users find products, answer questions about the store, and give purchase advice.",
        },
        {"role": "user", "content": payload.message},
    ]
    try:
        reply = await chat(messages)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"LLM gateway error: {e!s}. Check FreeLLMAPI configuration.",
        ) from e
    return {"reply": reply}
