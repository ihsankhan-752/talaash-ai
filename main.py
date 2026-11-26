from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.schemas import DealSearchRequest, DealSearchResponse
from app.agent import run_deal_search

app = FastAPI(
    title=settings.app_name,
    description="Autonomous cross-platform deal and price intelligence API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "model": settings.gemini_model,
    }


@app.post("/api/v1/deals/search", response_model=DealSearchResponse)
def search_deals(request: DealSearchRequest):
    try:
        return run_deal_search(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))