import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query: str, count: int = 5) -> str:
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "apiKey": NEWS_API_KEY,
            "pageSize": count,
            "sortBy": "publishedAt",
            "language": "en"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            return f"News API error: {data.get('message', 'Unknown error')}"

        articles = data.get("articles", [])
        if not articles:
            return f"'{query}' ke baare mein koi news nahi mili."

        output = f"Latest news for '{query}':\n\n"
        for i, article in enumerate(articles, 1):
            output += f"{i}. **{article['title']}**\n"
            output += f"   Source: {article['source']['name']}\n"
            output += f"   {article.get('description', 'No description')}\n"
            output += f"   URL: {article['url']}\n\n"

        return output

    except Exception as e:
        return f"News fetch error: {str(e)}"


def fetch_stock(symbol: str) -> str:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()

        chart = data.get("chart", {})
        result = chart.get("result", [])

        if not result:
            return f"Stock '{symbol}' ka data nahi mila."

        meta = result[0].get("meta", {})
        price = meta.get("regularMarketPrice", "N/A")
        prev_close = meta.get("chartPreviousClose", "N/A")
        currency = meta.get("currency", "USD")
        name = meta.get("longName", symbol)

        change = round(price - prev_close, 2) if isinstance(price, float) and isinstance(prev_close, float) else "N/A"
        change_pct = round((change / prev_close) * 100, 2) if isinstance(change, float) and prev_close else "N/A"

        return (
            f"📈 Stock Info: {name} ({symbol})\n"
            f"   Current Price: {price} {currency}\n"
            f"   Previous Close: {prev_close} {currency}\n"
            f"   Change: {change} ({change_pct}%)\n"
        )

    except Exception as e:
        return f"Stock fetch error: {str(e)}"


# Tool specs for LLM
FETCH_NEWS_TOOL = {
    "type": "function",
    "function": {
        "name": "fetch_news",
        "description": "Fetch latest news articles on any topic from the internet.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Topic to search news for"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of articles to fetch (default 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}

FETCH_STOCK_TOOL = {
    "type": "function",
    "function": {
        "name": "fetch_stock",
        "description": "Fetch current stock price and info for any stock symbol (e.g. AAPL, TSLA, RELIANCE.NS)",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol e.g. AAPL, TSLA, RELIANCE.NS, TCS.NS"
                }
            },
            "required": ["symbol"]
        }
    }
}