from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["products"])

# In-memory store for MVP (replace with DB later)
_products: dict[int, dict] = {}
_next_id = 1


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    price: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    category: str = "general"


class Product(ProductCreate):
    id: int


@router.get("/", response_model=list[Product])
async def list_products():
    return list(_products.values())


@router.post("/", response_model=Product, status_code=201)
async def create_product(payload: ProductCreate):
    global _next_id
    product = Product(id=_next_id, **payload.model_dump())
    _products[_next_id] = product.model_dump()
    _next_id += 1
    return product


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    return _products[product_id]


@router.patch("/{product_id}", response_model=Product)
async def update_product(product_id: int, payload: ProductCreate):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = Product(id=product_id, **payload.model_dump())
    _products[product_id] = updated.model_dump()
    return updated


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    del _products[product_id]
