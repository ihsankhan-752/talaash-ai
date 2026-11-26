




from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import httpx
from config import settings




@tool 
def calculate_net_deal(original_price: float, deal_price: float, shipping_cost:float = 0.0,) -> dict | str:
    """Calculate total landed cost, net savings, and exact discount percentage for a product deal."""
    if original_price<=0.0 or deal_price < 0:
        raise ValueError("Invalid price values provided")

    landed_cost = round(deal_price + shipping_cost, 2)
    net_saving = round(original_price - landed_cost, 2)
    discount_percent = round((net_saving / original_price) * 100, 1)

    return {
    "landed_cost": landed_cost,
    "net_saving": net_saving,
    "discount_percent": discount_percent,
    "is_real_deal": net_saving > 0,
}

@tool
def convert_currency(amount: float, from_currency: str, to_currency:str) -> dict | str:
    """Convert a monetary amount from one currency code (e.g., USD) to another (e.g., PKR, AED, EUR)."""

    source = from_currency.strip().upper()
    target = to_currency.strip().upper()

    try:
        response = httpx.get(f"https://open.er-api.com/v6/latest/{source}", timeout=10.0)
        data = response.json()
        rate = data.get("rates", {}).get(target)
        if rate is None:
            return f"Unsupported target currency: {target}"
        return {
            "original_amount": amount,
            "from_currency": source,
            "to_currency": target,
            "exchange_rate": rate,
            "converted_amount": round(amount * rate, 2),
        }
    except Exception as e:
        return f"Currency conversion failed: {str(e)}"

search_tool = TavilySearch(max_results = 3, tavily_api_key = settings.tavily_api_key )

tool = [search_tool,calculate_net_deal, convert_currency]
