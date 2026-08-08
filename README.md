# 📈 InsiderPulse — C-Suite Cluster Buy Browser Agent

> **Built for the Browser-use Hackathon (Delhi Edition)**  
> An autonomous AI browser agent that monitors SEC C-suite insider trades, validates live market momentum, and generates structured trade intelligence.

---

## 🎯 Overview

High-conviction C-suite insider buying (CEOs and CFOs purchasing their own company's stock on the open market) is one of the strongest fundamental signals in financial markets. However, manually cross-referencing SEC disclosures with real-time stock quotes across multiple tabs is tedious.

**InsiderPulse** automates this entire workflow using an AI-driven browser agent. Running live on Chromium, the agent:
1. Scraps open-market C-suite purchases exceeding **$100,000** from public filings.
2. Cross-references live market data on Yahoo Finance.
3. Compares the executive's purchase price against current market levels.
4. Generates a structured trade intelligence report—stopping safely before staging or executing orders.

---

## 🚀 Features

- **Autonomous Browser Control:** Driven by `browser-use` and Playwright to handle dynamic web elements directly in the DOM.
- **Zero API Ingestion Costs:** Powered by Google's free **Gemini 1.5 Flash** multimodal vision LLM.
- **Real-Time Data Cross-Referencing:** Multi-tab browser navigation between SEC summary tables and live market quotes.
- **Safety & Responsible AI:** Adheres to human-in-the-loop principles by synthesizing actionable insights without taking unprompted financial actions.

---

## 🛠️ Tech Stack

- **Framework:** [`browser-use`](https://github.com/browser-use/browser-use)
- **Browser Automation:** [Playwright (Chromium)](https://playwright.dev/)
- **LLM Engine:** [`langchain-google-genai`](https://github.com/langchain-ai/langchain) (Google Gemini 1.5 Flash)
- **Language & Runtime:** Python 3.10+

---

## 📋 Prerequisites

- **Python:** Version 3.10, 3.11, or 3.12 installed.
- **Google Gemini API Key:** Free key obtained from [Google AI Studio](https://aistudio.google.com).

---

## 📦 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/your-username/InsiderPulse.git](https://github.com/your-username/InsiderPulse.git)
   cd InsiderPulse
