import os
import re
import asyncio
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

def get_top_insider_trade():
    """Scrapes OpenInsider for the top CEO/CFO purchase over $100k."""
    url = "http://openinsider.com/top-insider-purchases-of-the-day"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table", {"class": "tinytable"})
    if not table:
        return None

    rows = table.find_all("tr")[1:] # Skip header
    for row in rows:
        cols = [td.text.strip() for td in row.find_all("td")]
        if len(cols) < 12:
            continue
        
        ticker = cols[3]
        title = cols[5]
        price_str = cols[8].replace("$", "").replace(",", "")
        value_str = cols[11].replace("$", "").replace(",", "")

        try:
            price = float(price_str)
            value = float(value_str)
        except ValueError:
            continue

        # Target CEO or CFO trades over $100,000
        if ("CEO" in title.upper() or "CFO" in title.upper()) and value > 100000:
            return {
                "ticker": ticker,
                "title": title,
                "buy_price": price,
                "total_value": value
            }
    return None

def get_live_price(ticker):
    """Fetches live stock quote from Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers).json()
    try:
        price = res['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except Exception:
        return None

async def generate_report():
    print("==================================================")
    print("🚀 Starting InsiderPulse (Fast & Reliable)")
    print("==================================================")

    print("🔍 Scraping OpenInsider for CEO/CFO trades...")
    trade = get_top_insider_trade()
    
    if not trade:
        print("❌ No matching trade found today.")
        return

    print(f"✅ Found Trade: {trade['ticker']} ({trade['title']})")
    print(f"🔍 Fetching current stock price for {trade['ticker']}...")
    current_price = get_live_price(trade['ticker']) or trade['buy_price']

    diff_pct = ((current_price - trade['buy_price']) / trade['buy_price']) * 100

    # Pass trade data to Gemini for analysis
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY
    )

    prompt = f"""
    Provide a 1-sentence strategic investment summary for this insider transaction:
    Ticker: {trade['ticker']}
    Executive: {trade['title']}
    Insider Buy Price: ${trade['buy_price']}
    Total Purchase Value: ${trade['value']:,}
    Current Market Price: ${current_price}
    Discount/Premium: {diff_pct:.2f}%
    """

    insight = await llm.ainvoke(prompt)

    print("\n--------------------------------------------------")
    print("INSIDER PULSE TRADE REPORT")
    print("--------------------------------------------------")
    print(f"• Ticker: {trade['ticker']}")
    print(f"• Executive: {trade['title']}")
    print(f"• Insider Buy Price: ${trade['buy_price']:.2f}")
    print(f"• Total Transaction Value: ${trade['total_value']:,.2f}")
    print(f"• Current Market Price: ${current_price:.2f}")
    print(f"• Discount/Premium: {diff_pct:+.2f}%")
    print(f"• Strategy Summary: {insight.content.strip()}")
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    asyncio.run(generate_report())