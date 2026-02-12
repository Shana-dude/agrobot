import requests
from .config import AGMARKNET_API_KEY

RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"

def get_tomato_prices():
    """
    Fetches real-time tomato prices from Agmarknet (via data.gov.in)
    """
    if not AGMARKNET_API_KEY:
        return "AGMARKNET_API_KEY not configured."

    url = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={AGMARKNET_API_KEY}&format=json&filters[commodity]=Tomato&limit=5"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"Market API Error: {response.status_code}"
        
        data = response.json()
        records = data.get("records", [])
        
        if not records:
            return "No recent tomato price data found in the market."

        analysis = "Real-time Tomato Market Update:\n"
        for rec in records:
            state = rec.get("state", "N/A")
            market = rec.get("market", "N/A")
            modal_price = rec.get("modal_price", "N/A")
            date = rec.get("arrival_date", "N/A")
            analysis += f"- {market}, {state}: ₹{modal_price}/quintal (as of {date})\n"
        
        return analysis

    except Exception as e:
        return f"Failed to fetch market data: {str(e)}"
