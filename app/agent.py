from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from app.config import settings
from app.tools import tools
from app.schemas import  DealSearchRequest,DealSearchResponse

SYSTEM_PROMPT = """You are Talaash AI, an autonomous shopping and deal-intelligence assistant.
Your goal is to find genuine, current product deals, verify exact savings, and return accurate prices in the user's requested currency.

Follow these strict execution rules:
1. Search Live Deals: Use the Tavily search tool to locate current product listings, prices, and promotions matching the user's query.
2. Verified URLs Only: Every URL in your output MUST come directly from the Tavily search results. Never guess, shorten, or fabricate root store domains (e.g., do not output generic "https://www.amazon.com" links).
3. Exact Discount Math: Whenever a listing includes both an original retail price and a discounted price (or shipping cost), call `calculate_net_deal` to verify the exact net savings and discount percentage. Never estimate percentages mentally.
4. Currency Conversion: If a product price is listed in a different currency than the user's requested `target_currency`, call `convert_currency` to convert both `original_price` and `deal_price` into `target_currency`.
5. No Hallucinated Prices: If an original price is unavailable, leave `original_price` and `discount_percentage` as null rather than inventing numbers.
6. Concise Output: Respect the requested `max_results` limit and provide clear, practical buying advice in `agent_notes`."""



llm = ChatGoogleGenerativeAI(api_key = settings.google_api_key, model = settings.gemini_model, temperature = 0)


deal_agent = create_agent(model = llm, tools = tools, system_prompt = SYSTEM_PROMPT, response_format = DealSearchResponse)

def run_deal_search(request: DealSearchRequest) -> DealSearchResponse:
    user_message = (
        f"Find up to {request.max_results} best current deals for: {request.query}. "
        f"Return all prices converted to {request.target_currency.upper()}."
    )
    result = deal_agent.invoke({
        "messages": [{"role": "user", "content": user_message}]
    })
    return result["structured_response"]