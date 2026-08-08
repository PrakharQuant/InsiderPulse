import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatGoogle

# Load environment variables
load_dotenv()

async def run_insider_pulse():
    # Retrieve key from .env (checks both GEMINI_API_KEY and GOOGLE_API_KEY)
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: API key is missing from .env file!")
        return

    # Use browser-use's native Google model class
    llm = ChatGoogle(
        model="gemini-1.5-flash",
        api_key=api_key,
    )

    # Launch browser in visible mode
    browser = Browser(headless=False)

    agent_task = """
    1. Go to http://openinsider.com/top-insider-purchases-of-the-day
    2. Scan the table for the top CEO or CFO stock purchase with a trade value over $100,000.
    3. Extract: Stock Ticker, Executive Title, Purchase Price, and Total Dollar Value.
    4. Open a new tab, navigate to https://finance.yahoo.com, and search for that Stock Ticker.
    5. Extract the live current stock price.
    6. Print a structured summary comparing the Executive Buy Price vs Current Market Price.
    """

    agent = Agent(task=agent_task, llm=llm, browser=browser)

    print("\n🚀 Launching InsiderPulse Agent...\n")
    result = await agent.run()
    
    print("\n================ FINAL INSIDER REPORT ================")
    print(result)
    print("======================================================\n")

if __name__ == "__main__":
    asyncio.run(run_insider_pulse())