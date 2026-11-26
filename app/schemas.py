from pydantic import BaseModel, Field


class DealSearchRequest(BaseModel):
    query: str = Field(description="Product or deal search query from the user")
    target_currency: str = Field(default="USD", description="3-letter currency code such as USD, PKR, or AED")
    max_results: int = Field(default=3, ge=1, le=10, description="Maximum number of deals to return")


class DealItem(BaseModel):
    product_name: str = Field(description="Exact name and model of the product")
    store: str = Field(description="Retailer or online store offering the deal")
    original_price: float | None = Field(default=None, description="Original retail price before discount, if available")
    deal_price: float = Field(description="Final deal price converted to the requested target currency")
    currency: str = Field(description="3-letter currency code of the displayed prices")
    discount_percentage: float | None = Field(default=None, description="Verified discount percentage from calculate_net_deal")
    url: str = Field(description="Direct product or deal page URL returned by search results")
    summary: str = Field(description="Concise 1-sentence reason why this deal is worth buying")


class DealSearchResponse(BaseModel):
    query: str
    target_currency: str
    deals: list[DealItem]
    agent_notes: str = Field(description="Brief buying advice or currency/shipping notes for the user")