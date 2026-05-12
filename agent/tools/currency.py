import requests

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    try:
        # Free API - no key needed
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if "rates" not in data:
            return "Currency data fetch nahi hua."

        rates = data["rates"]

        if to_currency.upper() not in rates:
            return f"Currency '{to_currency}' supported nahi hai."

        rate = rates[to_currency.upper()]
        converted = round(amount * rate, 2)

        return (
            f"💱 Currency Conversion:\n"
            f"   {amount} {from_currency.upper()} = {converted} {to_currency.upper()}\n"
            f"   Exchange Rate: 1 {from_currency.upper()} = {rate} {to_currency.upper()}\n"
        )

    except Exception as e:
        return f"Currency conversion error: {str(e)}"


CURRENCY_TOOL = {
    "type": "function",
    "function": {
        "name": "convert_currency",
        "description": "Convert currency from one type to another with live exchange rates. e.g. USD to INR, EUR to GBP",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount to convert"
                },
                "from_currency": {
                    "type": "string",
                    "description": "Source currency code e.g. USD, EUR, INR, GBP"
                },
                "to_currency": {
                    "type": "string",
                    "description": "Target currency code e.g. USD, EUR, INR, GBP"
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    }
}