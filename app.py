import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="InsiderPulse", page_icon="📈", layout="centered")
st.title("🚀 InsiderPulse Trade Scanner")

def get_top_insider_trade():
    url = "http://openinsider.com/top-insider-purchases-of-the-day"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "tinytable"})
    if not table:
        return None

    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = [td.text.strip() for td in row.find_all("td")]
        if len(cols) < 12:
            continue
        ticker, title = cols[3], cols[5]
        price_str = cols[8].replace("$", "").replace(",", "")
        value_str = cols[11].replace("$", "").replace(",", "")
        try:
            price, value = float(price_str), float(value_str)
        except ValueError:
            continue

        if ("CEO" in title.upper() or "CFO" in title.upper()) and value > 100000:
            return {"ticker": ticker, "title": title, "buy_price": price, "total_value": value}
    return None

def get_live_price(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers).json()
    try:
        return float(res['chart']['result'][0]['meta']['regularMarketPrice'])
    except Exception:
        return None

if st.button("Run Insider Pulse Scan", type="primary"):
    with st.spinner("Scraping market data and running Gemini analysis..."):
        trade = get_top_insider_trade()
        if not trade:
            st.error("No matching CEO/CFO trades over $100,000 found today.")
        else:
            current_price = get_live_price(trade['ticker']) or trade['buy_price']
            diff_pct = ((current_price - trade['buy_price']) / trade['buy_price']) * 100

            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)
            prompt = f"Provide a 1-sentence strategic summary for: Ticker {trade['ticker']}, Executive {trade['title']}, Buy Price ${trade['buy_price']}, Current Price ${current_price}, Discount/Premium {diff_pct:.2f}%."
            insight = llm.invoke(prompt)

            st.success("Scan Complete!")
            st.markdown("---")
            col1, col2 = st.columns(2)
            col1.metric("Ticker", trade['ticker'])
            col1.metric("Executive Title", trade['title'])
            col1.metric("Insider Buy Price", f"${trade['buy_price']:.2f}")

            col2.metric("Current Market Price", f"${current_price:.2f}")
            col2.metric("Total Transaction Value", f"${trade['total_value']:,.2f}")
            col2.metric("Discount / Premium", f"{diff_pct:+.2f}%")

            st.subheader("Strategy Summary")
            st.info(insight.content.strip())