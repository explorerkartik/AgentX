from ddgs import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "Koi result nahi mila."
        
        output = f"Search results for: '{query}'\n\n"
        for i, r in enumerate(results, 1):
            output += f"{i}. **{r['title']}**\n"
            output += f"   {r['body']}\n"
            output += f"   URL: {r['href']}\n\n"
        
        return output
    except Exception as e:
        return f"Search error: {str(e)}"


# Tool spec for LLM
WEB_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for any query. Use this to find current information, news, facts, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Number of results to return (default 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}