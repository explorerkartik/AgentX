import requests
from bs4 import BeautifulSoup

def summarize_website(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title = soup.title.string if soup.title else "No title"

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Extract main text
        text = soup.get_text(separator="\n", strip=True)

        # Clean up
        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 50]
        content = "\n".join(lines[:50])

        return (
            f"🌐 Website: {title}\n"
            f"🔗 URL: {url}\n\n"
            f"📄 Content:\n{content[:3000]}"
        )

    except Exception as e:
        return f"Website summarize error: {str(e)}"


WEB_SUMMARIZER_TOOL = {
    "type": "function",
    "function": {
        "name": "summarize_website",
        "description": "Fetch and summarize any website or URL. Use when user gives a URL or asks to summarize a webpage.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Full URL of the website to summarize e.g. https://example.com"
                }
            },
            "required": ["url"]
        }
    }
}